import time

import pyvjoy
import efficientnet


print("Starting...")
time.sleep(1);
print("1")
time.sleep(1);
print("2")
time.sleep(1);
print("3")

controller = pyvjoy.VJoyDevice(1)

###### Global variables

J_SENSITIVITY = 1

# Button variables
KEY_A = 1
KEY_B = 2
KEY_X = 3
KEY_Y = 4
KEY_PRESSED = True
KEY_RELEASED = False

# Trigger variables
TRIGGER_MAX = 0x8000
TRIGGER_MEDIUM = 0x5000
TRIGGER_LOW = 0x2000
TRIGGER_NONE = 0x0

'''
    wAxisX = Left X
    wAxisY = Left y
    wAxisZ = Left Trigger

    wAxisXRot = Right X
    wAxisXRot = Right Y
    wAxisZRot = Right Trigger

    0x8000 = 32768
'''

# Set default values of the joysticks
controller.data.wAxisX = 0x4000
controller.data.wAxisY = 0x4000
controller.data.wAxisXRot = 0x4000
controller.data.wAxisYRot = 0x4000
controller.update()


def test1():
    controller.data.wAxisZRot = TRIGGER_MAX
    controller.update()
    time.sleep(3)

    controller.data.wAxisX = 0x6000
    controller.data.wAxisZRot = TRIGGER_LOW
    controller.update()
    time.sleep(1)

    controller.data.wAxisX = 0x4000
    controller.data.wAxisZRot = TRIGGER_MEDIUM
    controller.update()
    time.sleep(4)

    controller.data.wAxisZRot = TRIGGER_NONE
    controller.update()
    print("Test done. . .")

test1()


"""
def d_forward(throttle):
    controller.data.wAxisZ = TRIGGER_NONE

def vehicle_turn(axis, scale, sensitivity):
'''
    param: axis         -> -1.0 or 1.0  (-1.0 = left  |  1.0 = right)
    param: scale        -> 0 to 16000   (0 = no turn  |  16000 = full turn)
    param: sensitivity  -> 0 to 10      (controls the smoothness of joystick movement)
'''

def d_backwards(throttle):
    controller.data.wAxisZRot = TRIGGER_NONE

def vehicle_brake(strength, handbrake=False):

def 
"""