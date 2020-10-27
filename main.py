import math
from time import time

import cv2

#import driverAI
from screenprocessing import screenshot, process_frame, persp_transform

# Starting point of the program
loop_time = time()
while True:
    frame = screenshot()
    laneImg = process_frame(frame)

    # Debug FPS counter
    cv2.putText(laneImg, 'FPS: {}'.format(math.floor(1 / (time() - loop_time))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    loop_time = time()

    # Debug windows
    # cv2.imshow("GTAI 5", laneImg)
    cv2.imshow("Birds Eye View", persp_transform(frame))

    # See if 'q' key is pressed to exit
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
