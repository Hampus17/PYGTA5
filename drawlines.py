import json

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw
import numpy as np


def draw_lane(arr):
    image = Image.open('tests/ds0/img/frame_1009.jpg.png')

    draw = ImageDraw.Draw(image)
    
    i = 0
    draw_color = (255, 0, 0)
    for points in arr:
        if i == 1:
            draw_color = (0, 0, 255)
        elif i == 2:
            draw_color = (0, 255, 0)
        elif i == 3:
            draw_color = (186, 85, 211)
        i = i + 1
        draw.polygon(points, fill=draw_color)

    image.show()

with open("tests/ds0/ann/frame_1009.jpg.png.json") as json_file:
    xys = []
    data = json.load(json_file)
    for obj in data['objects']:
        p = obj['points']
        points = p['exterior']
        coords = []
        for xy in points:
            coords.append(tuple(xy))
        xys.append(tuple(coords))
        
    print(xys)
    draw_lane(tuple(xys))
