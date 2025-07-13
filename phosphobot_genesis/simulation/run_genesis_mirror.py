import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import genesis as gs
import threading
from zmq_control.robot_listener import robot_state_listener
from zmq_control.shared_state import shared_joint_state
#"Jaw":          {"min": 1941, "max": 3403}
import numpy as np
joint_config = {
    "Rotation":     {"min": 740,  "max": 3455},
    "Pitch":        {"min": 961,  "max": 3329},
    "Elbow":        {"min": 889,  "max": 3078},
    "Wrist_Pitch":  {"min": 669,  "max": 3079},
    "Wrist_Roll":   {"min": 0,    "max": 4096},
    "Jaw":          {"min": 400, "max": 3403},
}

gs.init(backend=gs.cpu)
scene = gs.Scene(show_viewer=True)
scene.viewer.show_fps = False

plane = scene.add_entity(gs.morphs.Plane())
robot = scene.add_entity(
    gs.morphs.URDF(
        file="./urdf/so-100.urdf",
        fixed=True    
    )
)
scene.build()

jnt_names = ['Rotation', 'Pitch', 'Elbow', 'Wrist_Pitch', 'Wrist_Roll', 'Jaw']
dofs_idx = [robot.get_joint(name).dof_idx_local for name in jnt_names]

# Start robot state listener
threading.Thread(target=robot_state_listener, args=(jnt_names,), daemon=True).start()

def ticks_to_radians(tick, min_tick, max_tick):
    # Normalize to [-1, 1]
    center = (max_tick + min_tick) / 2.0
    half_range = (max_tick - min_tick) / 2.0
    normalized = (tick - center) / half_range
    max_rad = (max_tick - min_tick) / 4096.0 * 2 * np.pi / 2.0  # scaled to used range
    return normalized * max_rad

try:
    while True:
        joint_data_copy = shared_joint_state.get()
       
        pos_array = np.array([
            ticks_to_radians(
                shared_joint_state.get().get(j, (joint_config[j]["min"] + joint_config[j]["max"]) / 2),
                joint_config[j]["min"],
                joint_config[j]["max"]
            )
            for j in jnt_names
        ])


        for j, rad in zip(jnt_names, pos_array):
            print(f"{j}: {np.rad2deg(rad):.2f} degrees")


        robot.set_dofs_position(pos_array, dofs_idx)
        scene.step()

except KeyboardInterrupt:
    print("Shutting down...")

