import cv2 as cv2
import math
#import driver

from time import time
from screenprocessing import screenshot, proc_screenshot, warp_image

# Starting point of the program
loop_time = time()
while True:
    # 

    screen = screenshot()
    laneImg = proc_screenshot(screen)

    # Debug FPS counter
    cv2.putText(laneImg, 'FPS: {}'.format(math.floor(1 / (time() - loop_time))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    loop_time = time()

    # Debug windows
    cv2.imshow("Birds Eye View", warp_image(screen, False))
    cv2.imshow("GTAI 5", laneImg)

    # See if 'q' key is pressed to exit
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
