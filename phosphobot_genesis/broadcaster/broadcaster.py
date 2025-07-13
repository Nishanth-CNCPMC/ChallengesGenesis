import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append("/home/jbright/test_Ws/src/FTServo_Python")
import zmq
import time
from scservo_sdk import *
import json


# Setup serial port
try:
    portHandler = PortHandler('/dev/ttyACM0')
    packetHandler = sms_sts(portHandler)

    if portHandler.openPort():
        print("Port opened successfully.")
    else:
        raise RuntimeError("Failed to open port.")

    if portHandler.setBaudRate(1000000):
        print("Baudrate set successfully.")
    else:
        raise RuntimeError("Failed to set baudrate.")
except Exception as e:
    print(f"[ERROR] Serial setup failed: {e}")
    sys.exit(1)

# Setup ZMQ publisher
try:
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")
    print("[ZMQ] Broadcasting on tcp://*:5556")
except Exception as e:
    print(f"[ERROR] ZMQ setup failed: {e}")
    sys.exit(1)

# Function to read from servo
def read_servo(id):
    try:
        pos, _, comm_result, error = packetHandler.ReadPosSpeed(id)
        if comm_result != COMM_SUCCESS:
            print(f"[Servo {id}] Comm error: {packetHandler.getTxRxResult(comm_result)}")
        if error != 0:
            print(f"[Servo {id}] Packet error: {packetHandler.getRxPacketError(error)}")
        return pos
    except Exception as e:
        print(f"[Servo {id}] Read error: {e}")
        return 0

# Loop to broadcast servo positions
try:
    while True:
        joint_states = {
            "Rotation": read_servo(1),
            "Pitch": read_servo(2),
            "Elbow": read_servo(3),
            "Wrist_Pitch": read_servo(4),
            "Wrist_Roll": read_servo(5),
            "Jaw": read_servo(6)
        }
        print("[Broadcast] Joint states:", joint_states)
        topic = "robot_joint"
        message = json.dumps(joint_states)
        socket.send_string(f"{topic} {message}")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Exiting on user interrupt.")
finally:
    portHandler.closePort()

