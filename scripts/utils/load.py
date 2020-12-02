import os
import re
import json


def get_file_path(root_folder, user_id, system_id, model_id):
    correct_file = None

    regex_string = r"{:02}-{}-{}".format(user_id, system_id, model_id)

    # r=root, d=directories, f = files
    for r, d, f in os.walk(root_folder):
        for file in f:
            print(file)
            if '.json' in file:
                if re.search(regex_string, file) is not None:
                    correct_file = file

    if correct_file is None:
        print("file not found")
        return

    return os.path.join(root_folder, correct_file)

def try_load_data(full_path):
    if full_path is None:
        return None

    # Reading the json as a dict
    with open(full_path) as json_data:
        data = json.load(json_data)
    
    return data