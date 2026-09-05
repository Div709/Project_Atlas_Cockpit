import sys
import serial
import time

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout
)
# This is the engine that runs the graphical interface.
# It is the OS for the GUI

from PyQt6.QtCore import QTimer


arduino = serial.Serial("COM5", 9600)


class Cockpit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ATLAS COCKPIT")
        self.resize(400, 250)
        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
                color: lime;
                font-size: 16px;
            }
        """)

        self.title = QLabel("ATLAS COCKPIT")
        self.throttle = QLabel("Throttle: 0%")
        self.bar = QLabel("[----------]")

        self.raw = QLabel("Raw Value: 0")
        self.rpm = QLabel("RPM: 0")
        self.warning = QLabel("STATUS: NORMAL")
        self.status = QLabel("STATUS: READY")
        self.engine_state = "OFF"
        self.start_time = None
        self.last_button_state = 1


        layout = QVBoxLayout()
        layout.addWidget(self.bar)

        layout.addWidget(self.title)
        layout.addWidget(self.throttle)
        layout.addWidget(self.raw)
        layout.addWidget(self.status)
        layout.addWidget(self.warning)
        layout.addWidget(self.rpm)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100) # starts timer which runs ever 100ms

    def update_data(self):

        line = arduino.readline().decode().strip()
        print(line)

        parts = line.split(",")

        pot_value = int(parts[0].split("=")[1])
        engine_state = int(parts[1].split("=")[1])

        percent = int((pot_value / 1023) * 100)
        # Start engine

        # Detect button press edge

        if (
                engine_state == 0
                and self.last_button_state == 1
                and self.engine_state == "OFF"
        ):
            self.engine_state = "STARTING"
            self.start_time = time.time()

        self.last_button_state = engine_state


        # Engine starting

        if self.engine_state == "STARTING":

            self.status.setText("ENGINE: STARTING...")

            if time.time() - self.start_time > 2:
                self.engine_state = "RUNNING"

        # Engine running

        elif self.engine_state == "RUNNING":

            self.status.setText("ENGINE: RUNNING")

        # Engine off

        elif self.engine_state == "OFF":

            self.status.setText("ENGINE: OFF")

        print(self.engine_state)
        if self.engine_state == "RUNNING":
            rpm = int((percent / 100) * 5000)
        else:
            rpm = 0
        if rpm < 500:
            self.warning.setText("⚠ ENGINE IDLE")
            self.warning.setStyleSheet("color: yellow;")

        elif rpm > 4500:
            self.warning.setText("⚠ HIGH RPM WARNING")
            self.warning.setStyleSheet("color: red;")

        else:
            self.warning.setText("✅ SYSTEM NORMAL")
            self.warning.setStyleSheet("color: lime;")

        bars = int(percent / 10)

        gauge = "█" * bars + "░" * (10 - bars)

        self.throttle.setText(f"Throttle: {percent}%")
        self.bar.setText(gauge)
        self.raw.setText(f"Raw Value: {pot_value}")
        self.rpm.setText(f"RPM: {rpm}")



app = QApplication(sys.argv) # starts app

window = Cockpit()
window.show()

sys.exit(app.exec())