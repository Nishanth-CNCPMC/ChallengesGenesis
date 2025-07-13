# Phosphobot Genesis Control Suite

This repository provides a modular environment for robotic control and simulation using real-time servo integration, Genesis simulation, and ZMQ-based messaging. It was originally developed as a testbed and is now shared for replication, analysis, and further development.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/phosphobot_genesis.git
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

Once inside the `torch-env`, launch the backend server:
```bash
uvicorn server.main:app --reload
```

Then visit:

- **http://127.0.0.1:8000** – Main API server
- **http://127.0.0.1:8000/docs** – Swagger UI for testing endpoints

---

## 🧪 Challenges Overview

You can launch specific challenges either through API calls or by interacting with the server from a connected UI. Below is a breakdown of available tasks:

### 🔹 Challenge 1: Simulation Only
**Location:** `launch/challenge1.py`

- Launches a full Genesis simulation
- No hardware required
- Meant for motion planning and kinematic testing

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

### 🔹 Challenge 3: Under Development
There is no official implementation for Challenge 3. It was part of an earlier prototype phase and was **not finalized**.

- You can explore parts of the implementation in `misc/` and `zmq_control/`
- This challenge is **intended for manual interpretation and assessment** based on the existing codebase
- No automated or structured entry point exists for this challenge

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

This project was originally built as part of a technical test environment. Some modules may contain placeholder or test logic. Challenge 3 is intentionally left unfinished to allow open-ended interpretation and evaluation.

---

## 📜 License

MIT License (or add a custom license if applicable)

---

## ✍️ Contributing

If you find this helpful and want to improve or complete Challenge 3, feel free to fork, contribute, or open a pull request.
