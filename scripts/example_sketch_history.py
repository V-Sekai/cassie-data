import sys

from utils.load import *

# /!\ Polyscope is a dependency for this script! Install it: https://polyscope.run/py/installing/
from utils.polyscope_display import *

# DRAW PARAMETERS
draw_structured = True
skip_deleted = True


#### You can call this script from the command line, to load one of the sketches
#### Parameters:
####    user_id system_id model_id
####    OR file_name.json

def main(arg):
    print(SKETCH_HISTORY_FOLDER)
    if len(arg) == 3:
        print("Attempting to display model by user {} with system {} (model = {})".format(arg[0], arg[1], arg[2]))
        file_path = get_file_path(SKETCH_HISTORY_FOLDER, int(arg[0]), int(arg[1]), int(arg[2]))

    elif len(arg) == 1:
        print("Attempting to display model {}".format(arg[0]))
        file_path = os.path.join(SKETCH_HISTORY_FOLDER, arg[0])

    sketch_history = try_load_data(file_path)

    if sketch_history is None:
        print("Failed to load file")
        return

    # DRAW WITH POLYSCOPE
    polyscope_draw_all_sketch(sketch_history, draw_structured, skip_deleted)

if __name__ == '__main__':
    main(sys.argv[1:])