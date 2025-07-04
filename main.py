import threading
from datetime import datetime, timedelta
from pathlib import Path

import cv2

from PyQt6.QtCore import QTimer, pyqtSignal
from tello import TelloController, isPressed, set_style_param, APP_COLORS, set_frame_to_label
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from models.object_recognition import recognize_objects, speech
from ultralytics import YOLO

Form, Window = uic.loadUiType("tello.ui")
yolo_model = YOLO('yolov8n.pt')

def start_video_writer(frame_shape, relative_path: str, fps=30):
    """Initialize cv2.VideoWriter"""
    full_path = Path(__file__).parent / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    height, width = frame_shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # .mp4 format
    writer = cv2.VideoWriter(str(full_path), fourcc, fps, (width, height))
    return writer


class TelloGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TelloController()
        self.form = Form()
        self.form.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(50)

        self.last_frame = None
        self.form.screenshotButton.clicked.connect(self.screenshot_camera)
        self.form.takeOff.clicked.connect(self.takeoff)
        self.form.endFlight.clicked.connect(self.land)

        self.detected_labels = []
        self.speech_text = ''
        self.last_detection_time = datetime.now()

        self.thread = threading.Thread(target=self.run_speech, daemon=True)
        self.thread.start()


    def update_gui(self):
        self.set_frame()
        self.set_battery_level()

        if isPressed('m'):
            self.screenshot_camera()

        self.update_controls()

        state = get_tello_state(self.controller)
        displaySpeed = self.controller.get_speed()
        self.form.flightTime.setText(f'{self.controller.tello.get_flight_time()} seconds')
        self.form.speed.setText(f'Speed: {displaySpeed},\n {state}')


    def update_controls(self):
        if not self.controller.running: return

        speed = 200
        elevation_speed = 100
        yaw_speed = 70

        self.controller.update()
        if self.controller.land:
            self.land()
            return

        if not self.controller.isTakeoff and isPressed('t'):
            takeoff(self.controller)

        if self.controller.isTakeoff:
            self.controller.move_with(speed, elevation_speed, yaw_speed)


    def set_battery_level(self):
        self.form.battery.setValue(self.controller.tello.get_battery())

    def screenshot_camera(self):
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        relative_path = f'screenshots/tello-cam-{date}.png'
        # Resolve the full path relative to the repo root
        full_path = Path(__file__).parent / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        frame2 = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame2, (1280, 720))

        success = cv2.imwrite(str(full_path), frame)

        if not success:
            raise print(f"Failed to save image to {full_path}")

    def run_speech(self):
        while self.controller.running:
            if len(self.speech_text) > 0:
                speech(self.speech_text)


    def set_frame(self):
        widget = self.form.frameDisplay
        frame, yolo_labels = recognize_objects(self.controller.frame_read.frame, yolo_model, self.detected_labels)

        found_label = False
        new_objects = ''
        for label in yolo_labels:
            if label not in self.detected_labels:
                found_label = True
                new_objects += f'Found {label}, '
                self.detected_labels.append(label)

        if found_label:
            dT = datetime.now() - self.last_detection_time
            if dT > timedelta(seconds=10): #seconds
                self.speech_text = new_objects
                self.last_detection_time = datetime.now()

        # cache frame
        self.last_frame = frame
        set_frame_to_label(frame, widget)

    def land(self):
        self.controller.quit()

        self.form.takeOff.setText(f'Take Off')
        self.form.endFlight.setText(f'Landing...')

        set_style_param(self.form.takeOff, 'background-color', APP_COLORS['primary'])
        set_style_param(self.form.endFlight, 'background-color', APP_COLORS['inactive'])

    def takeoff(self):
        self.controller.takeoff()
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





app = QApplication([])
window = TelloGUI()

window.show()
app.exec()

cv2.destroyAllWindows()