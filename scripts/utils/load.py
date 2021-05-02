import os
import re
import json
import numpy as np

SKETCH_RAW_FOLDER = os.path.join(os.path.realpath('..'), 'data/raw_data')
SKETCH_HISTORY_FOLDER = os.path.join(os.path.realpath('..'), 'data/sketch_history')
SKETCH_GRAPH_FOLDER = os.path.join(os.path.realpath('..'), 'data/sketch_graph')
CURVES_FOLDER = os.path.join(os.path.realpath('..'), 'data/curves')

def get_file_path(root_folder, user_id, system_id, model_id, extension='json'):
    correct_file = None

    regex_string = r"{:02}-{}-{}".format(user_id, system_id, model_id)

    extension = '.' + extension

    # r=root, d=directories, f = files
    for r, d, f in os.walk(root_folder):
        for file in f:
            if extension in file:
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

def load_curves_data(path):
    if path is None:
        return None
    full_path = os.path.join(CURVES_FOLDER, path)
    
    polylines = []
    current_polyline = np.empty((0,3))
    target_vertex_count = -1

    with open(full_path) as f:
        for line in f:
            els = line.split()
            if els[0] == 'v':
                # Start a new polyline
                current_polyline = np.empty((0,3))
                target_vertex_count = int(els[1])
                
            else:
                if len(current_polyline) >= target_vertex_count:
                    print("error reading file, vertex count and actual vertex data is inconsistent.")
                    break
                # Parse vertex 3D position and add it to current polyline
                pos = np.array([float(els[i]) for i in range(3)])
                current_polyline = np.row_stack([current_polyline, pos])

                if len(current_polyline) == target_vertex_count:
                    polylines.append(current_polyline)

    return polylines

# Support different encoding of vec3, either a list or an object with the coordinates

def parse_vec3(vec3_object):
    if isinstance(vec3_object, list):
        return vec3_object
    else:
        return [vec3_object['x'], vec3_object['y'], vec3_object['z']]

def parse_ctrl_pts(ctrl_pts):
    return [[parse_vec3(p) for p in pts] for pts in ctrl_pts]