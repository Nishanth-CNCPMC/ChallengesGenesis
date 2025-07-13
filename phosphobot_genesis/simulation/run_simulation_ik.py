import zmq
import threading

import numpy as np
import sys
import os
import queue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("/home/jbright/Downloads/ompl-1.7.0/build/py-bindings")
import genesis as gs
from zmq_control.listener import start_listener
from simulation.sim_environment import scene, so100

os.environ["TI_LOG_LEVEL"] = "error"
motion_queue = queue.Queue()

# --- ZMQ Listener Thread ---
def start_motion_listener():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6000")
    while True:
        try:
            msg = socket.recv_json()
            x, y, z = msg["x"], msg["y"], msg["z"]
            print(f"[ZMQ] Received motion target: ({x}, {y}, {z})")
            motion_queue.put((x, y, z))
            socket.send_json({"status": "received"})
        except Exception as e:
            print(f"[ERROR] Exception in motion listener: {e}")
            socket.send_json({"status": "error", "message": str(e)})

# --- Print Joint Indices ---
for j in so100.joints:
    print(f"Joint: {j.name}, dof_idx_local: {j.dof_idx_local}")

# --- Joint Setup ---
jnt_names = ['Rotation', 'Pitch', 'Elbow', 'Wrist_Pitch', 'Wrist_Roll', 'Jaw']
dofs_idx = [so100.get_joint(name).dof_idx_local for name in jnt_names]
joint_map = {j.name: j for j in so100.joints}

# --- Start ZMQ Threads ---
threading.Thread(target=start_listener, args=(so100, jnt_names, dofs_idx), daemon=True).start()
threading.Thread(target=start_motion_listener, daemon=True).start()

# --- Main Genesis Loop ---
try:
    while True:
        if not motion_queue.empty():
            x, y, z = motion_queue.get()
            print(f"[Genesis] Executing motion to: ({x}, {y}, {z})")

            try:
                target_pos = np.array([x, y, z])
                target_quat = np.array([0, 1, 0, 0])
                end_effector = so100.get_link("Moving Jaw")

                qpos = so100.inverse_kinematics(link=end_effector, pos=target_pos, quat=target_quat)

                if qpos is not None:
                    qpos_np = qpos.cpu().numpy()
                    if not np.any(np.isnan(qpos_np)):
                        path = so100.plan_path(qpos_goal=qpos_np, num_waypoints=100)
                        for waypoint in path:
                            so100.control_dofs_position(waypoint)
                            scene.step()
                        for _ in range(30):
                            scene.step()
                        print("[Genesis] Target reached successfully")
                    else:
                        print("[Genesis] Invalid IK solution (NaNs in qpos)")
                else:
                    print("[Genesis] Invalid IK solution")

            except Exception as e:
                print(f"[ERROR] Failed to execute motion: {e}")

        scene.step()

except KeyboardInterrupt:
    print("Exiting simulation loop...")

