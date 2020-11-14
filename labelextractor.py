import json
import os
import sys

p_data = {
    'points': [

    ]
}

def extract(folder_path, proc_labelset_path, labelset_prefix):
    ''' 
        Used to extract and generate necessary information from JSON label file
        
        Parameters:
            folder_path (string): This is the path to the folder with the labelsets
            proc_labelset_path (string): Path to where processed labelsets are stored
            labelset_name (string): This is the prefix for the output labelsets
    '''
    
    
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            write_to = proc_labelset_path + "{}_frame.json".format(labelset_prefix)
            filepath = os.path.join(folder_path, file)
            with open(filepath) as json_file:
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
                        'lane_points' : coords
                        })
                    i = i + 1

            json_str = json.dumps(p_data, indent=4)
            with open(write_to, 'w') as outfile:
                outfile.write(json_str)
            continue
        else:
            print("Warning: Skipped {} (Not a JSON file)".format(file))
            continue
        
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4])