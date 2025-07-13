import numpy as np
import zmq
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time




sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["GENESIS_MAIN_PROCESS"] = "0"

from simulation.sim_environment import so100, scene  # assuming so100 is defined here
def handle_target_request(x, y, z, action="simulate"):
    target_pos = np.array([x, y, z])
    target_quat = np.array([0, 1, 0, 0])  # default orientation

    try:
        if so100 is None or scene is None:
            return {"status": "error", "message": "Simulation is not active in this process"}

        end_effector = so100.get_link("Moving Jaw")  # update if your link name differs

        # Solve IK
        qpos = so100.inverse_kinematics(
            link=end_effector,
            pos=target_pos,
            quat=target_quat
        )

        if qpos is None or np.any(np.isnan(qpos)):
            return {"status": "error", "message": "IK solution invalid or not found"}

        if action == "simulate":
            path = so100.plan_path(
                qpos_goal=qpos,
                num_waypoints=100
            )

            for waypoint in path:
                so100.control_dofs_position(waypoint)
                scene.step()

            for _ in range(100):
                scene.step()

            return {
                "status": "success",
                "message": "Simulated in Genesis (with IK and planning)",
                "joint_angles_rad": qpos.tolist()
            }

        elif action == "send":
            joint_names = ['Rotation', 'Pitch', 'Elbow', 'Wrist_Pitch', 'Wrist_Roll', 'Jaw']
            joint_angles_deg = {name: float(np.rad2deg(qpos[i])) for i, name in enumerate(joint_names)}

            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5555")
            socket.send_json(joint_angles_deg)
            ack = socket.recv_json()
            print("[ZMQ] Initial reply:", ack)

            POSITION_TOLERANCE = 0.5
            while True:
                time.sleep(0.1)
                socket.send_json({"query": True})
                current_state = socket.recv_json()
                reached = all(
                    abs(current_state.get(joint, 0.0) - target_angle) <= POSITION_TOLERANCE
                    for joint, target_angle in joint_angles_deg.items()
                )
                if reached:
                    print("[ZMQ] Target reached")
                    break

            return {
                "status": "success",
                "message": "Command sent and confirmed",
                "joint_angles_deg": list(joint_angles_deg.values())
            }

        else:
            return {"status": "error", "message": f"Invalid action: {action}"}

    except Exception as e:
        print("[ERROR] Exception during handle_target_request:", e)
        return {"status": "error", "message": str(e)}



