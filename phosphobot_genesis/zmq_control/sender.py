import zmq
import time
import numpy as np

# Set up ZMQ connection
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Define target positions (change values as needed)
target_commands = [
    {"Rotation": 0.5, "Elbow": -0.2},
    {"Rotation": 1.0, "Elbow": -0.5},
    {"Rotation": -0.5, "Elbow": 0.5},
    {"Rotation": 0.0, "Elbow": 0.0},
    {"Rotation": -1.0, "Elbow": -0.5},
]

# Define tolerance for joint convergence
POSITION_TOLERANCE = 0.02

# Loop indefinitely
try:
    while True:
        for target_cmd in target_commands:
            print(f"[ZMQ] Sending command: {target_cmd}")
            socket.send_json(target_cmd)
            reply = socket.recv_json()  # Expecting current joint positions
            print("[ZMQ] Initial Reply (Joint States):", reply)

            # Wait until the robot reaches the target
            while True:
                time.sleep(0.1)  # Avoid spamming
                socket.send_json({"query": True})  # Special key to request joint states
                current_state = socket.recv_json()

                # Check convergence
                reached = True
                for joint, target_val in target_cmd.items():
                    current_val = current_state.get(joint, 0.0)
                    if abs(current_val - target_val) > POSITION_TOLERANCE:
                        reached = False
                        break

                print("[ZMQ] Current:", current_state)

                if reached:
                    print("[ZMQ] Target reached, moving to next...\n")
                    break

except KeyboardInterrupt:
    print("Interrupted by user. Exiting.")

