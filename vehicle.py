import math
import time

import pyvjoy


class Vehicle:

    controller = pyvjoy.VJoyDevice(1)

    ###### Global variables
    STEER_SENSITIVITY = 1

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
    
    def __init__(self, mode, car_name="Unknown"):
        self.controller.data.wAxisX = 0x4000
        self.controller.data.wAxisY = 0x4000
        self.controller.data.wAxisXRot = 0x4000
        self.controller.data.wAxisYRot = 0x4000
        self.controller.update()
        print("vehicle created")

    def control_vehicle(self, predictions):
        '''
        Args:
            predictions: dict of predictions
        '''

        if predictions['forward'] is True:
            self.drive_forward(predictions['throttle'])
            print("Going forward")
        if predictions['forward'] is False:
            self.drive_backwards(predictions['throttle'])

        # Apply the correct steering radius
        self.turn(predictions['steering_scale'], 1)

        if predictions['steering_scale'] < 0:
            print("Turning left with:", predictions['steering_scale'])
        else:
            print("Turning right with:", predictions['steering_scale'])

        self.controller.update()

    def drive_forward(self, throttle):
        self.controller.data.wAxisZ = self.TRIGGER_NONE
        self.controller.data.wAxisZRot = throttle


    def turn(self, scale, sensitivity):
        '''
            param: axis         -> -1.0 or 1.0  (-1.0 = left  |  1.0 = right)
            param: scale        -> 0 to 16000   (0 = no turn  |  16000 = full turn)
            param: sensitivity  -> 0 to 10      (controls the smoothness of joystick movement)
        '''
        self.controller.data.wAxisX = math.floor(scale)

    def drive_backwards(self, throttle):
        self.controller.data.wAxisZRot = TRIGGER_NONE

    def brake(self, throttle, handbrake=False):
        pass

    def release_gas(self):
        self.controller.data.wAxisZRot = self.TRIGGER_NONE
        self.controller.data.wAxisZ = self.TRIGGER_NONE


    # def test1():
    #     self.controller.data.wAxisZRot = TRIGGER_MAX
    #     self.controller.update()
    #     time.sleep(3)
    #
    #     self.controller.data.wAxisX = 0x6000
    #     self.controller.data.wAxisZRot = TRIGGER_LOW
    #     self.controller.update()
    #     time.sleep(1)
    #
    #     self.controller.data.wAxisX = 0x4000
    #     self.controller.data.wAxisZRot = TRIGGER_MEDIUM
    #     self.controller.update()
    #     time.sleep(4)
    #
    #     self.controller.data.wAxisZRot = TRIGGER_NONE
    #     self.controller.update()
    #     print("Test done. . .")


