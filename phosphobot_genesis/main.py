from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import zmq
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "launch")))
from challenge1 import start_challenge_one, stop_challenge_one
from challenge2 import start_challenge_two, stop_challenge_two


app = FastAPI()
app.mount("/static", StaticFiles(directory="server/static"), name="static")
templates = Jinja2Templates(directory="server/templates")

# Setup ZMQ context and socket once
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:6000")  # This port must match the one in your motion listener

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    x: float = Form(...),
    y: float = Form(...),
    z: float = Form(...),
    action: str = Form(...)
):
    try:
        socket.send_json({"x": x, "y": y, "z": z})
        reply = socket.recv_json()
    except Exception as e:
        reply = {"status": "error", "message": str(e)}

    return templates.TemplateResponse("index.html", {"request": request, "result": reply})

@app.post("/simulate")
async def simulate_target(x: float = Form(...), y: float = Form(...), z: float = Form(...)):
    try:
        socket.send_json({"x": x, "y": y, "z": z})
        reply = socket.recv_json()
    except Exception as e:
        reply = {"status": "error", "message": str(e)}

    return JSONResponse(content=reply)

@app.post("/send")
async def send_target(x: float = Form(...), y: float = Form(...), z: float = Form(...)):
    try:
        socket.send_json({"x": x, "y": y, "z": z})
        reply = socket.recv_json()
    except Exception as e:
        reply = {"status": "error", "message": str(e)}

    return JSONResponse(content=reply)


@app.post("/start_challenge1")
async def start_challenge1():
    try:
        start_challenge_one()
        return JSONResponse(content={"status": "started"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

@app.post("/stop_challenge1")
async def stop_challenge1():
    try:
        stop_challenge_one()
        return JSONResponse(content={"status": "stopped"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

@app.post("/start_challenge2")
async def start_challenge2():
    try:
        success = start_challenge_two()
        if success:
            print("Challenge 2 started successfully.")
            return JSONResponse(content={"status": "started"})
        else:
            print("Failed to start Challenge 2. Check if the servo is connected to the correct port.")
            return JSONResponse(content={"status": "failed", "message": "Serial port not found or could not be opened."})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

@app.post("/stop_challenge2")
async def stop_challenge2():
    try:
        stop_challenge_two()

        return JSONResponse(content={"status": "stopped"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})
