import time

import keyboard
import cv2
from PIL.ImageQt import QImage, QPixmap
from djitellopy import Tello

APP_COLORS = {
    'primary': 'hsl(243, 37%, 52%)',
    'secondary': 'hsl(243, 37%, 52%)',
    'inactive': 'hsl(360, 10%, 30%)',
}

def set_style_param(widget, param: str, value: str):
    current_style = widget.styleSheet()
    lines = current_style.strip().splitlines()

    # Remove any existing line that sets this parameter
    lines = [line for line in lines if not line.strip().startswith(f"{param}:")]

    # Add the new parameter at the end
    lines.append(f"{param}: {value};")

    # Update the stylesheet
    widget.setStyleSheet("\n".join(lines))


def set_frame_to_label(frame, label):
    # Convert OpenCV BGR to RGB
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame2, (371, 251))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h, w, ch = rgb.shape
    bytes_per_line = ch * w

    # Create QImage
    qimage = QImage(rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

    # Create QPixmap and scale if needed
    pixmap = QPixmap.fromImage(qimage)
    label.setPixmap(pixmap)


def clamp(v, a, b):
    return a if v < a else b if v > b else v

def get_axis():
    horizontal = 0
    vertical = 0

    # Horizontal axis: A/D
    if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
        horizontal -= 1
    if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
        horizontal += 1

    # Vertical axis: W/S
    if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
        vertical += 1
    if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
        vertical -= 1

    return horizontal, vertical

def get_keys(a, b):
    elevation = 0
    if keyboard.is_pressed(a):
        elevation -= 1
    if keyboard.is_pressed(b):
        elevation += 1

    return elevation

def get_land():
    return keyboard.is_pressed('l')

def isPressed(key):
    return keyboard.is_pressed(key)



class TelloController:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.tello.streamon()
        self.tello.send_command_with_return("streamon")
        time.sleep(2)

        self.frame_read = self.tello.get_frame_read()

        self.right = 0.0
        self.forward = 0.0
        self.elevate = 0.0
        self.yaw = 0.0
        self.land = False
        self.running = True
        self.isTakeoff = False
        self.sensitivity = 1.0

        self.distX = 0.0
        self.distY = 0.0
        self.distZ = 0.0

        #self.video_thread = threading.Thread(target=self.video_loop)
        #self.video_thread.daemon = True
        #self.video_thread.start()

        print(f'Tello connected at {self.tello.get_battery()}')

    def takeoff(self):
        self.tello.takeoff()
        self.isTakeoff = True

    def update(self):
            horizontal, vertical = get_axis()
            self.right = horizontal
            self.forward = vertical
            self.elevate = get_keys('q', 'e')
            self.land = get_land()
            self.yaw = get_keys('u', 'o')

    def move_with(self, speed, elevation_speed, yaw_speed):
        self.tello.send_rc_control(self.right * speed, self.forward * speed,self.elevate * elevation_speed, self.yaw * yaw_speed)

    def get_speed(self):
        return self.tello.get_speed_x(), self.tello.get_speed_y(), self.tello.get_speed_z()

    def quit(self):
        self.running = False
        self.isTakeoff = False
        self.tello.streamoff()
        self.tello.land()
        self.tello.end()


