import json
import os
import sys
import pandas as pd

p_data = {
    "label": {
        
    }, 
    "xy_points": {
        
    },
    "num_of_points": {

    },
    "id": {

    }
}

def extract(folder_path, proc_labelset_path, labelset_prefix):
    ''' 
        Used to extract and generate necessary information from JSON label file
        
        Parameters:
            folder_path (string): This is the path to the folder with the labelsets
            proc_labelset_path (string): Path to where processed labelsets are stored
            labelset_name (string): This is the prefix for the output labelsets
    '''
    
    frame_count = 0
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            write_to = proc_labelset_path + "{}_frame{}".format(labelset_prefix, frame_count)
            filepath = os.path.join(folder_path, file)
            with open(filepath) as json_file:
                id = 0
                
                data = json.load(json_file)
                for obj_key in data['objects']:
                    points_key = obj_key['points']
                    label = obj_key['classTitle']
                    coords = []
                    points = 0
                    for point in points_key['exterior']:
                        coords.extend(point)
                        points += 1        
                    p_data["label"][id] = label
                    p_data["xy_points"][id] = coords
                    p_data["num_of_points"][id] = (points / 2)
                    p_data["id"][id] = (id + 1)
                    id += 1

            json_file = json.dumps(p_data, indent=4)
            json_df = pd.read_json(json_file)
            csv_file = json_df.to_csv()
            with open("{}.json".format(write_to), 'w') as outfile:
                outfile.write(json_file)
            with open("{}.csv".format(write_to), 'w') as outfile:
                outfile.write(csv_file)
            frame_count = frame_count + 1
            continue
        else:
            print("Warning: Skipped {} (Not a JSON file)".format(file))
            continue
        
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4])