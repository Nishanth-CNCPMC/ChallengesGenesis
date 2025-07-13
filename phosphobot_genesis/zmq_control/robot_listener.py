import zmq
import json
import time
from zmq_control.shared_state import shared_joint_state

def robot_state_listener(jnt_names):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt_string(zmq.SUBSCRIBE, "robot_joint")

    print("[ZMQ] Subscribed to robot joint state")
    time.sleep(0.5)

    while True:
        try:
            msg = socket.recv_string()
            _, json_str = msg.split(" ", 1)
            data = json.loads(json_str)
            filtered_data = {j: data.get(j, 0.0) for j in jnt_names}
            shared_joint_state.update(filtered_data)
        except Exception as e:
            print("[ZMQ] Error receiving message:", e)


