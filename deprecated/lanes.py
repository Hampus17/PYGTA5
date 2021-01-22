import json
import math

from PIL import ImageDraw, Image, ImageFilter

## Change so it can draw lines without JSON file as well (need ML first)
## Do so it can recieve a numpy image?

## Draw rectangle of the corner points (last and first corner) then check if middle of 
## screen is inside of it, or how much is inside of or something like that


TEST_LABEL_SET = "tests/PROCESSED_LABELSET/test_set1_frame.json"
TEST_IMAGE = "tests/IMAGES/frame_40088.jpg.png"

#### Maybe get average of the points of the line to get a more smooth line
### then check the tilt of the value to determine which way to steer?

def draw_lanes(image, label_set):
    '''
        Parameters:
            image (Image): The image which to draw the lanes on
            label_set (JSON): The labelset file which includes the lane points
    '''
    img = Image.open(image)
    i = 0
    draw_color = ()
    left_lane = None
    right_lane = None
    
    grouped_set = JSON_to_list(label_set)
    for group in grouped_set:
        if i == 0: draw_color = (0, 0, 255)
        elif i == 1: draw_color = (0, 255, 0)
        elif i == 2: draw_color = (255, 0, 0)
        else: draw_color = (186, 85, 211)

        if 'left_lane' in group[0]: left_lane = group[1]
        elif 'right_lane' in group[0]: right_lane = group[1]
        
        ImageDraw.Draw(img).line(tuple(group[1]), fill=draw_color, width=8)
    
        i = i + 1
    
    middle_lane = []
    iterations = len(right_lane) if len(left_lane) > len(right_lane) else len(left_lane)
        
    for x in range(iterations):
        temp_x = (left_lane[x][0] + right_lane[x][0]) / 2
        temp_y = (left_lane[x][1] + right_lane[x][1]) / 2
        
        middle_lane.append((temp_x, temp_y))
    
    ImageDraw.Draw(img).line(tuple(middle_lane), fill=(255, 255, 255), width=4)
    img = img.filter(ImageFilter.GaussianBlur(1))
    img.show()


def JSON_to_list(file):
    '''
        Used to extract the points for the lanes

        Parameters:
            file (JSON): JSON file that includes the XY points for the lanes
        
        Return(s):
             grouped_set (list): A list version of the JSON file
    '''

    with open(file) as json_file:
        grouped_set = []
        data = json.load(json_file)
        
        i = 1
        for lanes in data['points']:
            temp_set = []
            temp_set.append([lanes['label']])
            xy_set = []
            for xy in lanes['lane_points']:
                xy_set.append(tuple(xy))
            temp_set.append(xy_set)
            grouped_set.append(temp_set)
            i = i + 1
        
        return grouped_set
        # return tuple(xy_points)


draw_lanes(TEST_IMAGE, TEST_LABEL_SET)
