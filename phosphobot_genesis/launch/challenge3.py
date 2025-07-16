import os
import subprocess
import signal

# Global variable to track the subprocess
_simulation_process = None

def start_challenge_three():
    global _simulation_process

    if _simulation_process is not None and _simulation_process.poll() is None:
        print("Challenge 3 is already running.")
        return False

    script_path = os.path.join("simulation", "run_simulation_ik.py")
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return False

    try:
        _simulation_process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Allows killing the whole process group
        )
        print(f"Challenge 3 started with PID {_simulation_process.pid}")
        return True
    except Exception as e:
        print(f"Failed to start Challenge 3: {e}")
        return False

def stop_challenge_three():
    global _simulation_process

    if _simulation_process is None:
        print("Challenge 3 is not running.")
        return False

    if _simulation_process.poll() is not None:
        print("Challenge 3 process already exited.")
        _simulation_process = None
        return True

    try:
        print(f"Stopping Challenge 3 (PID {_simulation_process.pid})...")
        os.killpg(os.getpgid(_simulation_process.pid), signal.SIGTERM)  # Kill process group
        _simulation_process.wait(timeout=5)
        print("Challenge 3 terminated.")
        _simulation_process = None
        return True
    except Exception as e:
        print(f"Error stopping Challenge 3: {e}")
        return False

