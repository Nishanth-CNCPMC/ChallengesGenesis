import subprocess
import threading
import os

# Dictionary to track processes
challenge_two_procs = {}

def start_challenge_two():
    print("[CHALLENGE 2] Starting Real World Joint Integration...")

    broadcaster_path = os.path.join("broadcaster", "broadcaster.py")
    try:
        broadcaster_proc = subprocess.Popen(
            ["python3", broadcaster_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )
        challenge_two_procs["broadcaster"] = broadcaster_proc
        print("[CHALLENGE 2] broadcaster.py started with PID", broadcaster_proc.pid)
    except Exception as e:
        print(f"[CHALLENGE 2] Failed to start broadcaster.py: {e}")
        return False

    result = {"success": False}

    def monitor_broadcaster():
        try:
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
        except Exception as e:
            print(f"[CHALLENGE 2] Error while reading broadcaster output: {e}")
        finally:
            broadcaster_proc.wait()

    monitor_thread = threading.Thread(target=monitor_broadcaster)
    monitor_thread.start()
    monitor_thread.join(timeout=10)

    if not result["success"]:
        print("[CHALLENGE 2] Setup failed or timed out.")
        stop_challenge_two()

    return result["success"]

def launch_mirror():
    mirror_path = os.path.join("simulation", "run_genesis_mirror.py")
    try:
        mirror_proc = subprocess.Popen(
            ["python3", mirror_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )
        challenge_two_procs["mirror"] = mirror_proc
        print("[CHALLENGE 2] run_genesis_mirror.py started with PID", mirror_proc.pid)
    except Exception as e:
        print(f"[CHALLENGE 2] Failed to start run_genesis_mirror.py: {e}")
        return

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

