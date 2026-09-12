from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import serial

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
arduino = serial.Serial("COM5", 9600)
@app.get("/")
def home():
    return {
        "message": "Atlas Backend Running"
    }

@app.get("/telemetry")
def telemetry():

    line = arduino.readline().decode().strip()

    try:

        parts = line.split(",")

        return {
            "pot": int(parts[0].split("=")[1]),
            "state": parts[1].split("=")[1],
            "rpm": int(parts[2].split("=")[1])
        }

    except Exception as e:

        return {
            "error": str(e),
            "raw": line
        }