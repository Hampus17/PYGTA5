import numpy as np
import cv2 as cv2

from windowcapture import WindowCapture


wincap = WindowCapture("Grand Theft Auto V")

def screenshot():
	screen = np.array(wincap.get_screenshot())
	return screen


def proc_screenshot(screenshot):
    # Define ROI and apply it to the screenshot
    vertices = np.float32([
    	(0,screenshot.shape[0]),
    	(0, 340),
    	(360, 220),
    	(480, 220),
    	(screenshot.shape[1], 340),
    	(screenshot.shape[1], screenshot.shape[0])
	])
    screenshot = get_roi(screenshot, vertices)

    # LAB (Yellow), HSV (Yellow + white), HLS (Yellow + white), RGB (White)
    ### Convert screenshot to color spaces
    lab = cv2.cvtColor(screenshot, cv2.COLOR_RGB2LAB)
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
    hls = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HLS)

    ### Select color spaces
    L_lab, A_lab, B_lab = cv2.split(lab) # Yellow (LAB)
    H_hsv, S_hsv, V_hsv = cv2.split(hsv) # Yellow and White (HSV)
    H_hls, L_hls, S_hls = cv2.split(hls) # ... (HLS)

    ### Generate the thresholded binary images
    # Yellow (LAB)
    L_lab_max, L_lab_mean = np.max(L_lab), np.mean(L_lab)
    B_lab_max, B_lab_mean = np.max(B_lab), np.mean(B_lab)

    L_adapt = max(80, int(L_lab_max * 0.45))
    B_adapt =  max(int(B_lab_max * 0.75), int(B_lab_mean * 1))
    lab_low = np.array((L_adapt, 120, B_adapt))
    lab_high = np.array((255, 145, 255))

    lab_binary = get_binary_thresh(lab, lab_low, lab_high)

    # Yellow and White (HSV)

    return lab_binary


# Generate thresholded binary
def get_binary_thresh(image, low, high):

	# Check if image is grayscale
	if (len(image.shape) == 2):
		screenCopy = np.zeros_like(screenshot)
		binaryMask = (image >= low) & (image <= high)

	elif (len(image.shape) == 3):
		screenCopy = np.zeros_like(image)
		binaryMask = (image[:,:,0] >= low[0]) & (image[:,:,0] <= high[0]) \
			& (image[:,:,1] >= low[1]) & (image[:,:,1] <= high[1]) \
			& (image[:,:,2] >= low[2]) & (image[:,:,2] <= high[2])

	print(binaryMask)
	screenCopy[binaryMask] = 255
	return screenCopy


def get_roi(image, vertices):
    vertices = np.array(vertices, ndmin=3, dtype=np.int32)
    if len(image.shape) == 3:
        fill_color = (255,) * 3
    else:
        fill_color = 255
            
    mask = np.zeros_like(image)
    mask = cv2.fillPoly(mask, vertices, fill_color)
    return cv2.bitwise_and(image, mask)


# Warp the image to get a birds eye view of the road
def warp_image(image, visualize = False):
    '''
    :param image = The original image
    :param visualize = Boolean flag for visualization
    :return = Warped image
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