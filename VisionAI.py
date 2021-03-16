import numpy as np
import cv2

from lane_detection import *
from Vehicle import *

class VisionAI:

    def predict_lane(self, frame):

        birdView, birdViewL, birdViewR, minverse = perspectiveWarp(frame)

        img, hls, grayscale, thresh, blur, canny = processImage(birdView)

        hist, leftBase, rightBase = plotHistogram(thresh)
        plt.plot(hist)

        ploty, left_fit, right_fit, left_fitx, right_fitx = slide_window_search(thresh, hist)
        plt.plot(left_fit)

        draw_info = general_search(thresh, left_fit, right_fit)

        cRadius, cDirection = measure_lane_curvature(ploty, left_fitx, right_fitx)

        meanPts, result = draw_lane_lines(frame, thresh, minverse, draw_info)

        deviation, directionDev = offCenter(meanPts, frame) #get_position

        # finalImg = addText(result, cRadius, cDirection, deviation, directionDev)

        # print("Curve Radius:", cRadius)
        # print("Curve Direction:", cDirection)
        # print("Deviation:", deviation)
        # print("Turn Direction:", directionDev)

        cv2.imshow("Prediction", result)

        predictions = {
            "curve_radius": cRadius,
            "curve_direction": cDirection,
            "dist_from_middle": deviation # - => go right | + => go left
        }

        return predictions


    def predict_vehicle(self, frame):
        '''

        Returns: dict of predictions

        '''

        car_predictions = {}

        # Trigger variables
        TRIGGER_MAX = 0x8000
        TRIGGER_MEDIUM = 0x5000
        TRIGGER_LOW = 0x2000
        TRIGGER_NONE = 0x0

        steering_scale = 0 # Depending on the angle/slope of the lanes, look at which is more dominant
        forward = True
        throttle = 0x3500
        break_throttle = TRIGGER_NONE
        car_break = False

        lane_predictions = self.predict_lane(frame)

        ## Calculate the steering scale
        steering_scale = lane_predictions["dist_from_middle"] / 1000
        steering_scale = (steering_scale * 1600) * 1000

        ## Calculate throttle
        # For now fixed a low

        ## Calculate if car should go forward
        # For now fixed to always go forward

        car_predictions = {
            'steering_scale': steering_scale,
            'forward': forward,
            'throttle': throttle,
        }

        if car_break is False:
            car_predictions['break'] = False

        elif car_break is True:
            car_predictions['break'] = True
            car_predictions['break_throttle'] = break_throttle

        return car_predictions
