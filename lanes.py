import json

from PIL import ImageDraw, Image

## Change so it can draw lines without JSON file as well (need ML first)
## Do so it can recieve a numpy image?

TEST_LABEL_SET = "tests/PROCESSED_LABELS/xy_points.json"
TEST_IMAGE = "tests/IMAGES/frame_1009.jpg.png"

def draw_lanes(image, label_set):
    '''
        Parameters:
            image (Image): The image which to draw the lanes on
            label_set (List): The 
    '''
    img = Image.open(image)
    grouped_set = extract_lane_points(label_set)

    i = 0
    draw_color = (0, 0, 255)

    for xy_sets in grouped_set:
        if i == 1:
            draw_color = (0, 255, 0)
        elif i == 2:
            draw_color = (255, 0, 0)
        elif i == 3:
            draw_color = (186, 85, 211)
        i = i + 1
        ImageDraw.Draw(img).polygon(tuple(xy_sets[1]), fill=draw_color)

    img.show()


def extract_lane_points(file):
    '''
        Used to extract the points for the lanes

        Parameters:
            file (JSON): JSON file that includes the XY points for the lanes
        
        Return(s):
             xy_points (tuple): A tuple of XY points from JSON file
    '''

    with open(file) as json_file:
        grouped_set = []
        data = json.load(json_file)
        
        i = 1
        for lanes in data['points']:
            temp_set = []
            temp_set.append([lanes['label']])
            xy_set = []
            for xy in lanes['lane_{}'.format(i)]:
                xy_set.append(tuple(xy))
            temp_set.append(xy_set)
            grouped_set.append(temp_set)
            i = i + 1
        
        return grouped_set
        # return tuple(xy_points)


draw_lanes(TEST_IMAGE, TEST_LABEL_SET)