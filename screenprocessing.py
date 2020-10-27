import numpy as np
import cv2 as cv2

from windowcapture import WindowCapture


wincap = WindowCapture("Grand Theft Auto V")


def screenshot():
    screen = np.array(wincap.get_screenshot())
    return screen


def process_frame(frame):
    # Define ROI and apply it to the frame
    vertices = np.float32([
        (0, frame.shape[0]),
        (0, 340),
        (360, 220),
        (480, 220),
        (frame.shape[1], 340),
        (frame.shape[1], frame.shape[0])
    ])
    frame = get_roi(frame, vertices)

    # LAB (Yellow), HSV (Yellow + white), HLS (Yellow + white), RGB (White)
    # Convert screenshot to color spaces
    lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hls = cv2.cvtColor(frame, cv2.COLOR_RGB2HLS)

    # Select color spaces
    L_lab, A_lab, B_lab = cv2.split(lab)  # Yellow (LAB)
    H_hsv, S_hsv, V_hsv = cv2.split(hsv)  # Yellow and White (HSV)
    H_hls, L_hls, S_hls = cv2.split(hls)  # ... (HLS)

    # Generate the thresholded binary images
    # Yellow (LAB)
    L_lab_max, L_lab_mean = np.max(L_lab), np.mean(L_lab)
    B_lab_max, B_lab_mean = np.max(B_lab), np.mean(B_lab)

    L_lab_adapt = max(40, int(L_lab_max * 0.45))
    B_lab_adapt = max(int(B_lab_max * 0.75), int(B_lab_mean * 1))
    lab_low = np.array((L_lab_adapt, 120, B_lab_adapt))
    lab_high = np.array((255, 145, 255))

    lab_binary = get_binary_thresh(lab, lab_low, lab_high)

    # Yellow and White (HSV)

    return lab_binary


# Generate thresholded binary
def get_binary_thresh(image, low, high):

    # Check if image is grayscale
    if (len(image.shape) == 2):
        screen_copy = np.zeros_like(image)
        binary_mask = (image >= low) & (image <= high)

    elif (len(image.shape) == 3):
        screen_copy = np.zeros_like(image[:, :, 0])
        binary_mask = (image[:, :, 0] >= low[0]) & (image[:, :, 0] <= high[0]) \
            & (image[:, :, 1] >= low[1]) & (image[:, :, 1] <= high[1]) \
            & (image[:, :, 2] >= low[2]) & (image[:, :, 2] <= high[2])

    # print(binary_mask)
    screen_copy[binary_mask] = 1
    return screen_copy


def get_roi(image, vertices):
    vertices = np.array(vertices, ndmin=3, dtype=np.int32)
    if len(image.shape) == 3:
        fill_color = (255)
    else:
        fill_color = 255

    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask, vertices, fill_color)
    image = cv2.bitwise_and(image, mask)

    return image


# Warp the image to get a birds eye view of the road
def persp_transform(frame):
    '''
    :param frame = The original frame
    :param visualize = Boolean flag for visualization
    :return = Warped image
    '''

    ysize = frame.shape[0]
    xsize = frame.shape[1]

    src = np.float32(
        [[0, ysize / 1.5], 
        [xsize, ysize / 1.5], 
        [0, ysize / 2], 
        [xsize, ysize / 2]
    ])

    dst = np.float32(
        [[xsize / 3, ysize], 
        [xsize / 1.5, ysize], 
        [0, 0], [xsize, 0]
    ])

    roi_vertices = np.int32([
        [xsize - (xsize / 1.3), ysize],
        [xsize - (xsize / 1.3), 0],
        [xsize / 1.3, 0],
        [xsize / 1.3, ysize]
    ])

    # Compute and return the transformation matrix
    matrix = cv2.getPerspectiveTransform(src, dst)
    transformed_img = cv2.warpPerspective(frame, matrix, (xsize, ysize), flags=cv2.INTER_LINEAR)

    # return get_roi(transformed_img, roi_vertices)
    return transformed_img
