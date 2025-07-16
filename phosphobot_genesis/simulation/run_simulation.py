#./urdf/so-100.urdf
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import genesis as gs
import threading
from zmq_control.listener import start_listener
os.environ["TI_LOG_LEVEL"] = "error" 
from simulation.sim_environment import scene, so100

def print_gripper_tip():
    dofs = so100.get_dofs_position()
    T = so100.get_global_transform("Jaw")  
    offset = T @ np.array([0, 0, 0.08, 1.0])
    print(f"[GRIPPER TIP] Global position: {offset[:3]}")
    
# Print dof indices for debugging
for j in so100.joints:
    print(f"Joint: {j.name}, dof_idx_local: {j.dof_idx_local}")


# Manually list joint names that should be actuated (as per your URDF)
jnt_names = [
    'Rotation',
    'Pitch',
    'Elbow',
    'Wrist_Pitch',
    'Wrist_Roll',
    'Jaw',
]

# Get local dof indices for these joints
dofs_idx = [so100.get_joint(name).dof_idx_local for name in jnt_names]


# Create joint map for control
joint_map = {j.name: j for j in so100.joints}

# Run listener in a separate thread
threading.Thread(target=start_listener, args=(so100, jnt_names, dofs_idx), daemon=True).start()

# Run simulation indefinitely until Ctrl+C
try:
    while True:
        scene.step()
except KeyboardInterrupt:
    print("Exiting simulation loop...")


