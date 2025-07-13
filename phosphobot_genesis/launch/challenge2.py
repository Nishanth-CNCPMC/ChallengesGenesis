import subprocess
import threading
import time
import os
import signal

# Track the processes
challenge_two_procs = {}

def start_challenge_two():
    print("[CHALLENGE 2] Starting Real World Joint Integration...")

    broadcaster_path = os.path.join("broadcaster", "broadcaster.py")
    broadcaster_proc = subprocess.Popen(["python3", broadcaster_path],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        text=True,
                                        encoding="utf-8")
    challenge_two_procs["broadcaster"] = broadcaster_proc
    print("[CHALLENGE 2] broadcaster.py started with PID", broadcaster_proc.pid)

    result = {"success": False}

    def monitor_broadcaster():
        for line in broadcaster_proc.stdout:
            line = line.strip()
            print("[BROADCASTER OUT]", line)

            if "Port opened successfully." in line:
                result["success"] = True
                print("[CHALLENGE 2] Port found. Launching mirror...")
                launch_mirror()
                break

            if "[ERROR] Serial setup failed:" in line:
                print("[CHALLENGE 2] Serial setup failed.")
                break

        broadcaster_proc.wait()

    monitor_thread = threading.Thread(target=monitor_broadcaster)
    monitor_thread.start()
    monitor_thread.join(timeout=10)

    if not result["success"]:
        stop_challenge_two()

    return result["success"]


def launch_mirror():
    mirror_path = os.path.join("simulation", "run_genesis_mirror.py")
    mirror_proc = subprocess.Popen(["python3", mirror_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    challenge_two_procs["mirror"] = mirror_proc
    print("[CHALLENGE 2] run_genesis_mirror.py started with PID", mirror_proc.pid)

    def log_mirror_output():
        for line in mirror_proc.stdout:
            print("[MIRROR OUT]", line.strip())

    threading.Thread(target=log_mirror_output, daemon=True).start()

def stop_challenge_two():
    print("[CHALLENGE 2] Stopping Real World Joint Integration...")
    for name, proc in challenge_two_procs.items():
        if proc.poll() is None:
            print(f"[CHALLENGE 2] Terminating {name}.py (PID {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
                print(f"[CHALLENGE 2] {name}.py terminated cleanly.")
            except subprocess.TimeoutExpired:
                print(f"[CHALLENGE 2] {name}.py did not terminate in time. Killing forcefully.")
                proc.kill()
        else:
            print(f"[CHALLENGE 2] {name}.py already stopped.")

    challenge_two_procs.clear()
    print("[CHALLENGE 2] All processes stopped.")

if __name__ == "__main__":
    try:
        start_challenge_two()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_challenge_two()
