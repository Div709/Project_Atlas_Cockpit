from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import serial
import threading
import pygame
import threading

app = FastAPI()

control_throttle = 0

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

arduino = serial.Serial(
    "COM7",
    115200,
    timeout=1
)

latest_data = {
    "POT": "0",
    "STATE": "OFF",
    "RPM": "0",
    "AX": "0",
    "AY": "0",
    "AZ": "0"
}



def controller_reader():

    global controller_throttle

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller detected")
        return

    js = pygame.joystick.Joystick(0)
    js.init()

    print("Controller Connected")

    while True:

        pygame.event.pump()

        axis = js.get_axis(1)

        throttle = int(
            ((-axis + 1) / 2) * 100
        )

        controller_throttle = throttle
# ==================================
# BACKGROUND SERIAL READER
# ==================================
def serial_reader():

    global latest_data

    while True:

        try:

            line = (
                arduino.readline()
                .decode("utf-8", errors="ignore")
                .strip()
            )

            if not line.startswith("POT="):
                continue

            parts = line.split(",")

            data = {}

            for part in parts:

                if "=" in part:

                    key, value = part.split("=", 1)

                    data[key] = value

            latest_data = data

        except:
            pass

threading.Thread(
    target=serial_reader,
    daemon=True
).start()
threading.Thread(
    target=controller_reader,
    daemon=True
).start()


# ==================================
# API
# ==================================

@app.get("/")
def home():

    return {
        "status": "Atlas V2 Online"
    }

@app.get("/telemetry")
def telemetry():

    return latest_data
@app.get("/controller")
def controller():

    return {
        "throttle": controller_throttle
    }