import subprocess
import time
import threading
import os
import signal

# Store processes globally
challenge_one_procs = {}

def start_challenge_one():
    print("[CHALLENGE 1] Starting Simulation Setup...")

    # Launch simulation
    sim_path = os.path.join("simulation", "run_simulation.py")
    sim_proc = subprocess.Popen(["python3", sim_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    challenge_one_procs["simulation"] = sim_proc
    print("[CHALLENGE 1] run_simulation.py started with PID", sim_proc.pid)
    launch_sender()

def launch_sender():
    sender_path = os.path.join("zmq_control", "sender.py")
    sender_proc = subprocess.Popen(["python3", sender_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    challenge_one_procs["sender"] = sender_proc
    print("[CHALLENGE 1] sender.py started with PID", sender_proc.pid)

    def log_sender_output():
        for line in sender_proc.stdout:
            print("[SENDER OUT]", line.strip())
    threading.Thread(target=log_sender_output, daemon=True).start()

def stop_challenge_one():
    print("[CHALLENGE 1] Stopping Simulation Setup...")
    for name, proc in challenge_one_procs.items():
        if proc.poll() is None:
            print(f"[CHALLENGE 1] Terminating {name}.py (PID {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
                print(f"[CHALLENGE 1] {name}.py terminated cleanly.")
            except subprocess.TimeoutExpired:
                print(f"[CHALLENGE 1] {name}.py did not terminate in time. Killing forcefully.")
                proc.kill()
        else:
            print(f"[CHALLENGE 1] {name}.py already stopped.")

    challenge_one_procs.clear()
    print("[CHALLENGE 1] All processes stopped.")

