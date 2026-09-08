import sys
import serial
import time
from PyQt6.QtCore import Qt

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
        self.resize(800, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #202020;
                color: lime;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        self.title = QLabel("ATLAS COCKPIT")
        self.throttle = QLabel("Throttle: 0%")
        self.bar = QLabel("[----------]")
        self.raw = QLabel("Raw Value: 0")
        self.rpm = QLabel("0000 RPM")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rpm.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.throttle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rpm.setStyleSheet("""
                font-size: 40px;
                font-weight: bold;
                color: cyan;
                """)
        self.throttle.setStyleSheet("""
                font-size: 22px;#
                """)
        self.warning = QLabel("STATUS: NORMAL")
        self.status = QLabel("STATUS: READY")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.power_led = QLabel("● POWER")
        self.engine_led = QLabel("● ENGINE")
        self.warning_led = QLabel("● WARNING")
        self.power_led.setStyleSheet("color: green; font-size: 22px;")



        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.throttle)
        layout.addWidget(self.bar)
        layout.addWidget(self.raw)
        layout.addWidget(self.status)
        layout.addWidget(self.warning)
        layout.addWidget(self.rpm)
        layout.addWidget(self.power_led)
        layout.addWidget(self.engine_led)
        layout.addWidget(self.warning_led)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100) # starts timer which runs ever 100ms

    def update_data(self):

        try:
            line = arduino.readline().decode().strip()
            print(line)

            parts = line.split(",")

            pot_value = int(parts[0].split("=")[1])
            engine_state = parts[1].split("=")[1]
            rpm_from_arduino = int(parts[2].split("=")[1])
        except Exception as e:
            print(e)
            return

        percent = int((pot_value / 1023) * 100)
        # Start engine

        # Detect button press edge

        if engine_state == "OFF":
            self.status.setText("ENGINE: OFF")

        elif engine_state == "STARTING":
            self.status.setText("ENGINE: STARTING...")

        elif engine_state == "RUNNING":
            self.status.setText("ENGINE: RUNNING")

        if engine_state == "RUNNING":
            self.engine_led.setStyleSheet(
                "color: green; font-size:22px;"
            )
        else:
            self.engine_led.setStyleSheet(
                "color: gray; font-size:22px;"
            )



        rpm = rpm_from_arduino

        if rpm < 500:
            self.warning.setText("⚠ ENGINE IDLE")
            self.warning.setStyleSheet("color: yellow;")
            self.warning_led.setStyleSheet(
                "color: yellow; font-size:22px;"
            )

        elif rpm > 4500:
            self.warning.setText("⚠ HIGH RPM WARNING")
            self.warning.setStyleSheet("color: red;")
            self.warning_led.setStyleSheet(
                "color: red; font-size:22px;"
            )

        else:
            self.warning.setText("✅ SYSTEM NORMAL")
            self.warning.setStyleSheet("color: lime;")
            self.warning_led.setStyleSheet(
                "color: gray; font-size:22px;"
            )

        bars = int(percent / 10)

        gauge = "█" * bars + "░" * (10 - bars)

        self.throttle.setText(f"Throttle: {percent}%")
        self.bar.setText(gauge)
        self.raw.setText(f"Raw Value: {pot_value}")
        self.rpm.setText(f"{rpm:04d}RPM")



app = QApplication(sys.argv) # starts app

window = Cockpit()
window.show()

sys.exit(app.exec())