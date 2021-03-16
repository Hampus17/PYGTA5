import numpy as np
import cv2
import copy
import math

def roi(image, vertices):
    mask = np.zeros_like(image)
    mask_color = (255, 255, 255)
    cv2.fillPoly(mask, vertices, mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def get_left_right_lines(image, lines):
    blank_image = np.zeros((image.shape[0],image.shape[1],3),dtype=np.uint8)
    
    positive_slope_lines = []
    negative_slope_lines = []
    slopes = []
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope, line_length, y_intercept = get_slope_and_length(x1,y1,x2,y2)
            if abs(slope) == math.inf:
                    slope = 9999
            if slope != 0 and abs(y_intercept) != math.inf:
                if slope > 0:
                    positive_slope_lines.append((slope, y_intercept, line_length))
                else:
                    negative_slope_lines.append((slope, y_intercept, line_length))

    right_line_params = get_average_slope_and_intercept(positive_slope_lines) if len(positive_slope_lines)>0 else None
    left_line_params = get_average_slope_and_intercept(negative_slope_lines) if len(negative_slope_lines)>0 else None
    
    return left_line_params, right_line_params



def get_average_slope_and_intercept(line_slope_list):
    weighted_sum_slope = 0
    weighted_sum_intercept = 0
    sum_len = 0
   
    for slope, y_intercept, line_length in line_slope_list:
        weighted_sum_slope += slope*line_length
        weighted_sum_intercept += y_intercept*line_length
        sum_len += line_length
    
    return (weighted_sum_slope/sum_len), (weighted_sum_intercept/sum_len)
    

def get_slope_and_length(x1,y1,x2,y2):
    slope = (y2-y1)/(x2-x1)
    y_intercept = y1 - (slope*x1)
    line_length = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    return slope, line_length, y_intercept


def draw_lines(image, lines, og_image):
    image = copy.deepcopy(image)
    blank_image = np.zeros((image.shape[0],image.shape[1],3),dtype=np.uint8)
    
    slope = []
    intercept = []

    left_right_lines = get_left_right_lines(image, lines)
    line_coordinates = []
    
    if left_right_lines[0] != None and left_right_lines[1] != None:
        starty = image.shape[0]
        endy = int(0.50*image.shape[0])
        for slope, intercept in left_right_lines:
            startx = int((starty - intercept)/slope)
            endx = int((endy - intercept)/slope)
            line_coordinates.append([startx, starty, endx, endy])
            cv2.line(blank_image, (startx,starty), (endx,endy), (255, 0, 0), 10)
        
        og_image = cv2.addWeighted(blank_image, 0.6, og_image, 1, 0.0)
    return og_image, line_coordinates


def draw_lines_for_warped_image(image, lines):
    image = copy.deepcopy(image)
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    
    slope = []
    intercept = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            M =  (y2-y1)/(x2-x1)
            if abs(M) == math.inf:
                M = 9999
            if M != 0:
                slope.append(M)
                C = y1 - (M*x1)
                intercept.append(C)
                starty = image.shape[0]
                endy = int(0.5*image.shape[0])
                startx = int((starty - C)/M)
                endx = int((endy - C)/M)
                cv2.line(blank_image, (startx, starty), (endx, endy), (255, 0, 0), 3)

    image = cv2.addWeighted(image, 0.8, blank_image, 1, 0.0)
    return image


#### masking to make select white and yellow lines
def select_white_yellow(image):
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    # white color mask
    lower = np.uint8([0, 150,  0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(converted, lower, upper)

    # yellow color mask
    lower = np.uint8([16, 41, 133])
    upper = np.uint8([50, 255, 255])
    yellow_mask = cv2.inRange(converted, lower, upper)

    # combine the mask
    combined_mask = np.zeros((image.shape[0], image.shape[1], 3))
    combined_mask[(white_mask >= 200) | (yellow_mask >= 200)] = [255, 255, 255]

    return combined_mask, white_mask, yellow_mask


def get_src_destpoints_for_warping(image, line_coordinates):
    left_lane_cord = line_coordinates[0]
    right_lane_cord = line_coordinates[1]
    offset = 0
    #src_points = np.float32([[left_lane_cord[0]-offset, left_lane_cord[1]],
    #                       [left_lane_cord[2]-offset, left_lane_cord[3]-offset],
    #                       [right_lane_cord[2]+offset, right_lane_cord[3]-offset],
    #                       [right_lane_cord[0]+offset, right_lane_cord[1]],
    #                      ])
    
    src_points = np.float32([[int(image.shape[1]/2 - 400), int(image.shape[0])],
                           [int(image.shape[1]/2 - 200), int(0.75*image.shape[0])],
                           [int(image.shape[1]/2 + 300), int(0.75*image.shape[0])],
                           [int(image.shape[1]/2 + 600), int(image.shape[0])]
                          ])
    
    
    dest_img_size = 300
    dest_points = np.float32([[0, dest_img_size], 
                           [0, 0],
                           [dest_img_size, 0], 
                           [dest_img_size, dest_img_size],
                          ])
    
    return src_points, dest_points, dest_img_size


def warp_and_process_image(image, line_coordinates, src_points, dest_points, dest_img_size, white_yellow_mask_bin):
    warped_image, inv_homograpy_mat = getwarped_image(src_points, dest_points, white_yellow_mask_bin, dest_img_size)
    
    height_warp_img = warped_image.shape[0]
    width_warp_img = warped_image.shape[1]
    
    turn = find_turn(warped_image)
    overlayed_image = overlay_lane_color(image, line_coordinates)

    return warped_image, overlayed_image, turn

def getwarped_image(src_points, dest_points, image, dest_img_size):
    H = cv2.getPerspectiveTransform(src_points, dest_points)
    inv_H = cv2.getPerspectiveTransform(dest_points, src_points)
    warped_image = cv2.warpPerspective(image, H, (dest_img_size,dest_img_size))
    return warped_image, inv_H

def find_turn(image):
    gray = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    #canny_edges = cv2.Canny(image,100, 200)
    turn = None

    lines = cv2.HoughLinesP(gray,
                            rho=6,
                            theta=np.pi / 60,
                            threshold=250,
                            lines=np.array([]),
                            minLineLength=30,
                            maxLineGap=30)
    if lines is not None:
            left_line_params, right_line_params = get_left_right_lines(image, lines)
            if left_line_params is not None and right_line_params is not None:
                if left_line_params[0] < 0 and right_line_params[0] < 0:
                    turn = 'Turn Left'
                elif left_line_params[0] > 0 and right_line_params[0] > 0:
                    turn = 'Turn Right'
                else:
                    turn = 'Drive Straight'
   
    return turn

def overlay_lane_color(image, line_coordinates):
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    left_lane_cord = line_coordinates[0]
    right_lane_cord = line_coordinates[1]
    vertices = np.array([[left_lane_cord[0], left_lane_cord[1]],
                [left_lane_cord[2], left_lane_cord[3]],
                [right_lane_cord[2], right_lane_cord[3]],
                [right_lane_cord[0], right_lane_cord[1]]
               ])
    
    overlaying_color = (0, 255, 0)
    blank_image = cv2.fillPoly(blank_image, [vertices], overlaying_color)
    image = cv2.addWeighted(blank_image, 0.3, image, 1, 0.0)

    return image


