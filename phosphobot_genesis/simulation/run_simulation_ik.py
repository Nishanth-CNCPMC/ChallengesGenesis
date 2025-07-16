import numpy as np
import genesis as gs
from sim_environment import scene, so100 
from scipy.spatial.transform import Rotation as R

# Define DOF indices 
motors_dof = np.arange(6)  # 6 DOFs as per the URDF

# Set gains (tune as needed)
so100.set_dofs_kp(np.array([3000, 3000, 2500, 2000, 1500, 100]))
so100.set_dofs_kv(np.array([300, 300, 250, 200, 150, 10]))
so100.set_dofs_force_range(np.array([-50]*6), np.array([50]*6))

end_effector = so100.get_link("Fixed_Jaw")

# Base position (current)
initial_pos = np.array([0.0, -0.3, 0.02])
delta = 0.05  # 5 cm

# Set initial direction
direction = 1

while True:
    # Toggle direction
    direction *= -1

    # Compute new target position
    target_pos = initial_pos + np.array([direction * delta, 0.0, 0.0])

    # Inverse Kinematics 
    qpos = so100.inverse_kinematics(
        link=end_effector,
        pos=target_pos
    )

    # Move to target
    so100.control_dofs_position(qpos[:6])
    for _ in range(100):
        scene.step()

    # Optional: wait a bit at each end
    for _ in range(20):
        scene.step()

