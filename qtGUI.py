import random
import threading
import time

import cv2
from PyQt6.QtCore import QTimer, pyqtSignal

from tello import TelloController, isPressed, set_style_param, set_frame_to_label, APP_COLORS
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

Form, Window = uic.loadUiType("tello.ui")

class TelloGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form = Form()
        self.form.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.battery = 0
        self.form.endFlight.clicked.connect(self.land)
        self.form.takeOff.clicked.connect(self.takeoff)

    def update(self):
        if isPressed('d'):
            self.battery = random.randint(0, 100)

        self.battery = (self.battery + 1) % 100
        self.form.battery.setValue(self.battery)

    def set_frame(self):
        widget = self.form.frameDisplay

    def land(self):
        self.form.takeOff.setText(f'Take Off')
        self.form.endFlight.setText(f'Landing...')

        set_style_param(self.form.takeOff, 'background-color', APP_COLORS['primary'])
        set_style_param(self.form.endFlight, 'background-color', APP_COLORS['inactive'])

    def takeoff(self):
        self.form.takeOff.setText(f'In Flight')
        self.form.endFlight.setText(f'Land Drone')

        set_style_param(self.form.endFlight, 'background-color', APP_COLORS['primary'])
        set_style_param(self.form.takeOff, 'background-color', APP_COLORS['inactive'])





app = QApplication([])
window = TelloGUI()

window.show()
app.exec()