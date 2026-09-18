from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import serial
import threading

app = FastAPI()

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