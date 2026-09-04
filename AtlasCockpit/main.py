import sys
import serial

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import QTimer


arduino = serial.Serial("COM5", 9600)


class Cockpit(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ATLAS COCKPIT")
        self.resize(400, 250)

        self.title = QLabel("ATLAS COCKPIT")
        self.throttle = QLabel("Throttle: 0%")
        self.raw = QLabel("Raw Value: 0")
        self.status = QLabel("STATUS: READY")

        layout = QVBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.throttle)
        layout.addWidget(self.raw)
        layout.addWidget(self.status)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def update_data(self):
        try:
            line = arduino.readline().decode().strip()

            if line.startswith("POT="):

                value = int(line.split("=")[1])

                percent = int((value / 1023) * 100)

                self.throttle.setText(
                    f"Throttle: {percent}%"
                )

                self.raw.setText(
                    f"Raw Value: {value}"
                )

        except:
            pass


app = QApplication(sys.argv)

window = Cockpit()
window.show()

sys.exit(app.exec())