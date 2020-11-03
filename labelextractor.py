import json

p_data = {
    'points': [

    ]
}

def extract(file_to_read, file_to_write):
    ''' 
        Used to extract and generate necessary information from JSON label file
        
        Parameters:
            file_to_read (JSON): This is the original label file generated
            file_to_write (JSON): File to write the simplified version with only the necessary information
    '''
    with open(file_to_read) as json_file:
        i = 1
        data = json.load(json_file)
        for obj_key in data['objects']:
            points_key = obj_key['points']
            class_key = obj_key['classTitle']
            coords = []
            for point in points_key['exterior']:
                coords.append(point) 
            p_data['points'].append({
                'label' : class_key,
                'lane_{}'.format(i) : coords
                })
            i = i + 1

        json_str = json.dumps(p_data, indent=4)
        print(json_str)
        with open(file_to_write, 'w') as outfile:
            outfile.write(json_str)
