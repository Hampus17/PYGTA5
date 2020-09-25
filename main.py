import numpy as np
import cv2 as cv2
import math
import matplotlib.pyplot as plt

from time import time
from window_capture import WindowCapture


wincap = WindowCapture("Grand Theft Auto V")

#### TODO
# def go_straight():
# def go_left():
# def go_right():
# def go_backwards():
# def fit_curve():


# Draw the lanes on the original image (for debug purposes)
def draw_lanes(image, lines):
    try:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(image, 'Lines: Detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)

    except:
        cv2.putText(image, 'Lines: Not Detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        pass


# Process the image to get it ready for lane calculations
def proc_image(image):
    return 0


def calc_image(image):
    return 0

def get_roi(image, vertices):
    vertices = np.array(vertices, ndmin=3, dtype=np.int32)
    if len(image.shape) == 3:
        fill_color = (255,) * 3
    else:
        fill_color = 255
            
    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask, vertices, fill_color)
    return cv2.bitwise_and(image, mask)

'''
ROI vertices = np.float32([
    (0,screenshot.shape[0]),
    (0, 340),
    (360, 220),
    (480, 220),
    (screenshot.shape[1], 340),
    (screenshot.shape[1], screenshot.shape[0])
])
'''
# Warp the image to get a birds eye view of the road
def warp_image(image, visualize = False):
    '''
    :param image => original image
    :param visualize => Boolean flag for visualization
    :return => Warped image
    '''

    ysize = image.shape[0]
    xsize = image.shape[1]

    # Source points
    src = np.float32([
        (0, 500),
        (360, 220),
        (480, 220),
        (xsize, 500),
    ])

    # Destination points
    dst = np.float32([
        (350, ysize),
        (350, 220),
        (xsize - 350, 220),
        (xsize - 350, ysize)
    ])
    
    M = cv2.getPerspectiveTransform(src, dst)
    warpedimage = cv2.warpPerspective(image, M, (xsize, ysize), flags=cv2.INTER_LINEAR)

    roivertices = np.int32([
        [300, ysize],
        [300, 300],
        [xsize - 300, 300],
        [xsize - 300, ysize]
    ])

    warpedimage = get_roi(warpedimage, roivertices)

    return warpedimage


# Starting point of the program
loop_time = time()
while True:
    screenshot = np.array(wincap.get_screenshot())
    procLaneImg = proc_image(screenshot)

    # Debug FPS counter
    cv2.putText(procLaneImg, 'FPS: {}'.format(math.floor(1 / (time() - loop_time))), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
    loop_time = time()

    # Debug windows
    cv2.imshow("Birds Eye View", warp_image(screenshot, False))
    cv2.imshow("GTAI 5", screenshot)

    # See if 'q' key is pressed to exit
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
