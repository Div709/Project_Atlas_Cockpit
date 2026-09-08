from fastapi import FastAPI
import serial

app = FastAPI()

arduino = serial.Serial("COM5", 9600)

@app.get("/telemetry")
def telemetry():

    line = arduino.readline().decode().strip()

    print("RAW:", line)

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