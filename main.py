import threading
import time

import cv2
from PyQt6.QtCore import QTimer, pyqtSignal

from tello import TelloController, isPressed, set_style_param, APP_COLORS, set_frame_to_label
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

Form, Window = uic.loadUiType("tello.ui")

class TelloGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TelloController()
        self.form = Form()
        self.form.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.form.takeOff.clicked.connect(self.takeoff)
        self.form.endFlight.clicked.connect(self.land)

    def update(self):
        self.set_frame()

    def set_battery_level(self):
        self.form.battery.setValue(self.controller.tello.get_battery())

    def set_frame(self):
        widget = self.form.frameDisplay
        frame = self.controller.frame_read.frame
        set_frame_to_label(frame, widget)

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


def get_tello_state(controller:TelloController):
    btr = controller.tello.get_battery()
    height = controller.tello.get_height()
    dist = controller.tello.get_distance_tof()
    temp = controller.tello.get_temperature()
    fly_time = controller.tello.get_flight_time()
    return btr, height, dist, temp, fly_time


def takeoff(controller:TelloController):
    controller.takeoff()


def land_drone(controller:TelloController):
    controller.quit()


def update_loop(w:TelloGUI):
    w.form.takeOff.clicked.connect(takeoff(w.controller))
    w.form.endFlight.clicked.connect(land_drone(w.controller))

    delay = 0.05
    speed = 100
    elevation_speed = 50
    yaw_speed = 20

    initial_height = 35
    hover_time = 5
    start_time = time.time()

    print('thread call')
    while True:
        curr_time = time.time()
        w.controller.update()
        #print(get_tello_state())
        #if curr_time - start_time > hover_time: break
        if w.controller.land: break

        power = w.controller.tello.get_battery()
        state = get_tello_state(w.controller)
        displaySpeed = w.controller.get_speed()

        w.form.flightTime.setText(f'{w.controller.tello.get_flight_time()} seconds')
        w.form.speed.setText(f'Speed: {displaySpeed},\n {state}')

        if not w.controller.isTakeoff and isPressed('t'):
            takeoff(w.controller)

        if w.controller.isTakeoff:
            w.controller.move_with(speed, elevation_speed, yaw_speed)

        time.sleep(0.05)  # 20fps


    w.controller.quit()


app = QApplication([])
window = TelloGUI()

thread = threading.Thread(target=update_loop(window), daemon=True)
thread.start()

window.show()
app.exec()