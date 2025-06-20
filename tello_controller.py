from datetime import datetime
from pathlib import Path

from djitellopy import Tello
import time
import keyboard
import cv2

# KEYS
# W - FORWARD, S - BACKWARD
# A - LEFT, D - RIGHT,
# L - TURN RIGHT, J - TURN LEFT
# Z - FLY DOWN, C - FLY UP
# T - TAKE OFF
# F - LAND
# Q - END DRONE
# P - SCREENSHOT

tello = Tello()

tello.streamon()
time.sleep(2) # sleep for a while whilst tello gets frame reader

frame_reader = tello.get_frame_read()


def get_keys(a, b):
    elevation = 0
    if keyboard.is_pressed(a):
        elevation -= 1
    if keyboard.is_pressed(b):
        elevation += 1

    return elevation

def isPressed(key):
    return keyboard.is_pressed(key)


def right():
    return get_keys('a', 'd')

def forward():
    return get_keys('s', 'w')

def turn():
    return get_keys('j', 'l')

def elevate():
    return get_keys('z', 'c')

def land():
    return isPressed('F')

def screenshot_camera():
    frame = frame_reader.frame

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    relative_path = f'screenshots/tello-cam-{date}.png'
    # Resolve the full path relative to the repo root
    full_path = Path(__file__).parent / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame2, (1280, 720))

    success = cv2.imwrite(str(full_path), frame)

    if not success:
        raise print(f"Failed to save image to {full_path}")


# Code Stats Here
speed = 200
thrust = 100
turn_speed = 75

running = True
in_flight = False

while running:
    if not running: break
    if not in_flight:
        if isPressed('t'):
            tello.takeoff()
            in_flight = True
        else: continue

    if isPressed('q'):
        running = False
        break

    if land():
        tello.land()
        in_flight = False

    tello.send_rc_control(right() * speed, forward() * speed, elevate() * thrust, turn() * turn_speed)
    if isPressed('p'):
        screenshot_camera()



tello.land()
tello.streamoff()
tello.end()




