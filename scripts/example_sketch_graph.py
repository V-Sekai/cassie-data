import sys

from utils.load import *

# /!\ Polyscope is a dependency for this script! Install it: https://polyscope.run/py/installing/
from utils.polyscope_display import *


#### You can call this script from the command line, to load one of the sketches
#### Parameters:
####    user_id system_id model_id (system_id must be 1 or 2!)
####    OR file_name.json

def main(arg):

    if len(arg) == 3:
        print("Attempting to display model by user {} with system {} (model = {})".format(arg[0], arg[1], arg[2]))
        file_path = get_file_path(SKETCH_GRAPH_FOLDER, int(arg[0]), int(arg[1]), int(arg[2]))

    elif len(arg) == 1:
        print("Attempting to display model {}".format(arg[0]))
        file_path = os.path.join(SKETCH_GRAPH_FOLDER, arg[0])

    else:
        print("Please provide arguments to load a file. Defaulting to hat.json")
        file_path = os.path.join(SKETCH_GRAPH_FOLDER, "hat.json")

    sketch_graph = try_load_data(file_path)

    if sketch_graph is None:
        print("Failed to load file")
        return

    # DRAW WITH POLYSCOPE
    polyscope_draw_sketch_graph(sketch_graph)

if __name__ == '__main__':
    main(sys.argv[1:])