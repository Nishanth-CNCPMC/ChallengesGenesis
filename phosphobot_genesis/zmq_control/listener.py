import zmq
import traceback
import numpy as np


def start_listener(entity, jnt_names, dofs_idx):
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        print("[ZMQ] Listening on tcp://*:5555")
        
        while True:
            message = socket.recv_json()
            print("[ZMQ] Received:", message)

            if "query" in message:
                current_pos = entity.get_dofs_position(dofs_idx)
                socket.send_json({jnt: float(pos) for jnt, pos in zip(jnt_names, current_pos)})
                continue

            try:
                cmd = [message.get(jnt, 0.0) for jnt in jnt_names]
                entity.control_dofs_position(np.array(cmd), dofs_idx)
                print(f"[ZMQ] Applied control: {cmd}")
                socket.send_json({"status": "OK"})
            except Exception:
                print("[ZMQ] Failed to apply control:")
                traceback.print_exc()
                socket.send_json({"status": "ERROR"})

    except Exception:
        print("[ZMQ] Listener crashed:")
        traceback.print_exc()

