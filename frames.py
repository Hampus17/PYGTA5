import numpy as np
import cv2 as cv2
import scipy

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

    # Apply color mask
        # Yellow and white

    # Apply sobel filter

    # Combine sobel filter and color mask

    return frame


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
