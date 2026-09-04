import sys
import serial

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
        self.status = QLabel("STATUS: READY")

        layout = QVBoxLayout()
        layout.addWidget(self.bar)

        layout.addWidget(self.title)
        layout.addWidget(self.throttle)
        layout.addWidget(self.raw)
        layout.addWidget(self.status)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100) # starts timer which runs ever 100ms

    def update_data(self):
        try:
            line = arduino.readline().decode().strip() # reading of data
            # .readline() reads one line from arduino
            #decode() converts bytes which is sent by arduino into text
            # strip() removes /n

            if line.startswith("POT="):
                # only continues when POT = a value


                value = int(line.split("=")[1])
                # extracting the number
                # index 1 is taken which is the value. POT = 420. 420 is the value

                percent = int((value / 1023) * 100)
                bars = int(percent / 10)

                gauge = "█" * bars + "░" * (10 - bars)
                self.bar.setText(gauge)

                self.throttle.setText(
                    f"Throttle: {percent}%" # updating value
                )

                self.raw.setText(
                    f"Raw Value: {value}"
                )

        except: # error handling
            pass


app = QApplication(sys.argv) # starts app

window = Cockpit()
window.show()

sys.exit(app.exec())