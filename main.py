import time
import math
import traceback

import cv2
import numpy as np

from VisionAI import VisionAI
from capture import WindowCapture
from Vehicle import Vehicle

Wincap = WindowCapture("Grand Theft Auto V")

ai = VisionAI()
car = Vehicle(mode="Civilian", car_name="Roadster")

print("Starting")
time.sleep(1)
print("1")
time.sleep(1)
print("2")
time.sleep(1)
print("Started...")

loop_time = time.time()
while True:
    frame = np.array(Wincap.get_screenshot())

    try:
        predictions = ai.predict_vehicle(frame)
        car.control_vehicle(predictions)
    except:
        traceback.print_exc()

    #if time.time() % 2:
    #    print("Loops-per-second:", math.floor(1 / (time.time() - loop_time)))
    #loop_time = time.time()

    #laneDetection.processImage(frame)

    #processed_img = ai.process_frame(frame)

    #car.drive(ai.predict_vehicle())

    # Debug FPS counter
    # cv2.putText(laneImg, 'FPS: {}'.format(math.floor(1 / (time() - loop_time))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)


    # Debug windows
    #cv2.imshow("WY", processed_img["white_yellow_img"])
    #cv2.imshow("Canny", processed_img["canny_img"])
    #cv2.imshow("dwad0", processed_img["roi_image"])

    # See if 'q' key is pressed to exit
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
