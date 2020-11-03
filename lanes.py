import json
import cv2

from PIL import Image, ImageDraw
import numpy as np

## Change this so it works with feeding in a image and a JSON file
## Change so it can draw lines without JSON file as well 

def draw_lanes(image, points):
    '''
        This function is mostly used for debug purposes

        Parameters:
            image (Image): The image which to draw the lanes on
            points (tuple): The tuple of XY points for the lanes
    '''

    i = 0
    draw_color = (0, 0, 255)

    for xys in points:
        if i == 1:
            draw_color = (0, 255, 0)
        elif i == 2:
            draw_color = (255, 0, 0)
        elif i == 3:
            draw_color = (186, 85, 211)
        i = i + 1
        ImageDraw.Draw(image).polygon(xys, fill=draw_color)

    image.show()


def load_lane_points(file):
    '''
        Used to extract the points for the lanes

        Parameters:
            file (JSON): JSON file that includes the XY points for the lanes
        
        Return(s):
             xy_points (tuple): A tuple of XY points from JSON file
    '''

    with open(file) as json_file:
        xy_points = []
        data = json.load(json_file)
        for obj_key in data['objects']:
            points_key = obj_key['points']
            coords = []
            for point in points_key['exterior']:
                coords.append(tuple(point))
            xy_points.append(tuple(coords))

        return tuple(xy_points)


test_image = Image.open('tests/ds0/img/frame_1009.jpg.png')
test_json_file = "tests/ds0/ann/frame_1009.jpg.png.json"

draw_lanes(test_image, load_lane_points(test_json_file))
