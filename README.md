# Phosphobot Genesis Control Suite

This repository provides a modular environment for robotic control and simulation using real-time servo integration, Genesis simulation, and ZMQ-based messaging. 

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Nishanth-CNCPMC/ChallengesGenesis.git
cd phosphobot_genesis
```

### 2. Set Up the Environment with Conda

Make sure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed.

Then create the environment using the provided `torch.yml` file:
```bash
conda env create -f torch.yml
conda activate torch-env
```

This will install all required dependencies including PyTorch and other scientific libraries.

---

## 🖥️ Running the FastAPI Server

Make sure to install pyserial, python-multipart and check for any dependency errors while running the fast api server.

Once inside the `torch-env`, launch the backend server:
```bash
uvicorn server.main:app --reload
```
<img src="controlcenter'.png" alt="Axibo Control Center UI" style="width:80%; margin-top:10px;"/>
Then visit:

- **http://127.0.0.1:8000** – Main API server
- **http://127.0.0.1:8000/docs** – Swagger UI for testing endpoints

---

## 🧪 Challenges Overview

You can launch specific challenges either through API calls or by interacting with the server from a connected UI. Below is a breakdown of available tasks:

### 🔹 Challenge 1: Simulation Only
**Location:** `launch/challenge1.py`

- Launches a full Genesis simulation
- Load the URDF for the SO101 arm
- Expose Joints for real time ineractions with FK

### 🔹 Challenge 2: Real-World Joint Integration
**Location:** `launch/challenge2.py`

- Interfaces with servo motors over `/dev/ttyACM0`
- Starts `broadcaster/broadcaster.py` to read real servo joint states
- Waits for the serial port to be successfully opened before launching simulation mirroring via `simulation/run_genesis_mirror.py`
- Only launches the mirror if hardware is detected
- ZMQ is used to sync real joint positions with simulation

Make sure your servos are:

- Connected via USB
- Assigned correct IDs (1–6)
- Powered on

### 🔹 Challenge 3: Inverse Kinematics using OMPL
**Location:** `launch/challenge3.py`

- Install OMPL (Motion Planner Dependency) by following another repo of mine (https://github.com/Nishanth-CNCPMC/OMPL_Genesis_Installation.git)
- Runs simulation/run_simulation_ik.py to perform oscillating end-effector motion using inverse kinematics
- Moves the robot's end effector back and forth along the X-axis by 5 cm starting from 0.00, -0.30, 0.02
- Continuously toggles between two X positions using the Fixed_Jaw link
- Simulated motion uses Genesis physics and mimics real-world constraints

---

## 📁 Directory Structure

```
phosphobot_genesis/
├── broadcaster/              # Publishes real joint states via ZMQ
├── launch/                   # Launchers for challenge scripts
├── simulation/               # Genesis simulation logic and runners
├── server/                   # FastAPI backend server
├── zmq_control/              # ZMQ-based robot control and listeners
├── misc/                     # Extra utility and test scripts
├── urdf/                     # URDFs and STL meshes for the robot arm
├── main.py                   # Optional launcher
└── torch.yml                 # Conda environment definition
```

---

## 🛠 Hardware Requirements

For Challenge 2, you need:

- A USB-serial connection to servos (`/dev/ttyACM0`)
- Serial-compatible servo motors using `scservo_sdk`
- Servo IDs: Rotation(1), Pitch(2), Elbow(3), Wrist Pitch(4), Wrist Roll(5), Jaw(6)

---

## 🔗 Useful Endpoints

Example HTTP request to start Challenge 2:
```bash
POST http://localhost:8000/start_challenge2
```

Returns:
```json
{"status": "started"} // or "failed", "error"}
```

---

## 🧑‍🔬 Acknowledgments

This project was originally built as part of a technical test environment.

---

