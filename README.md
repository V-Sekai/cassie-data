# CASSIE - VR sketch data

This repository contains the dataset from the CASSIE project, both raw data recorded directly from our VR sketching app, along with data that has been reformated and compacted for easier downstream analysis of the sketches. Some example scripts are included to show how the data can be loaded and displayed.

We provide data for:

* 48 sketches done by 12 participants during a controlled user study (the task was to take max 5 minutes to sketch a running shoe or a desk lamp using 3 variants of the CASSIE system)
* 16 sketches done to demonstrate the overall system (the models are varied and the sketches are more complex)

More details about the CASSIE project: link to paper

Explore all the sketches directly in your browser: [CASSIE data website](http://www-sop.inria.fr/members/Emilie.Yu/CASSIE-sketch-explorer/)

## About the data

All sketches were collected in our custom VR sketching system, and are not representative of all VR sketching practices in a general context. In particular, the 36 sketches done in *Armature* and *Patch* mode from the study, and the 16 varied sketches were created using specific features from CASSIE that aimed to **help and encourage users to create well-connected curve networks** by sketching. Furthermore, we instructed participants to adopt a **sparse sketching style** in their drawings.

## Data

The data files available are, for each sketch, in 3 sub-folders:

* `raw_data` : direct export from CASSIE interactive applications, in the form of a full history of actions undertaken by the user during this session, and lists of primitives (strokes and patches) created (NB: the mesh for each patch was not recorded).
* `sketch_history` : a list of all strokes sketched during the session, along with creation/deletion time (if deleted), and both the raw input samples captured from the controller position and the structured result outputed by CASSIE (in the form of a poly-Bézier or line).
* `sketch_graph` : lists of strokes, graph segments and graph nodes that describe the connectivity structure of the sketch (NB: only available for study sketches for now).

For most purposes, the data from `sketch_history` folder should contain all necessary data. For example, these files are used to visualize sketching sessions on the [CASSIE data website](http://www-sop.inria.fr/members/Emilie.Yu/CASSIE-sketch-explorer/).

Each of the 3 folders has a README detailing the specific schema used for the data.

## Scripts

The folder `scripts` contains python scripts that can be used to load and display sketch data, using either [polyscope](https://github.com/nmwsharp/polyscope) or [pythreejs](https://github.com/jupyter-widgets/pythreejs) widgets in a Jupyter Notebook.

For example, you can try to display a sketch by running *(NB: needs polyscope to run)*:

```bash
# Display the hat sketch
> python3 example_sketch_history.py "hat.json"

# Display the sketch from participant 9, done with the Armature system (1), of the shoe model (2)
> python3 example_sketch_history.py 9 1 2
```

Or launch the jupyter notebook `Example - sketch history with pythreejs.ipynb` *(NB: needs pythreejs to run)*.

## File naming convention

In each folder, there is one `json` file per sketch.

The files from the study follow the naming convention:

`Participant ID - System ID - Model ID .json`

With the following code for the systems:

* *Freehand* = 0
* *Armature* (automatic structuring of the strokes) = 1
* *Patch* (automatic structuring + surface inference) = 2

And for the models:

* Lamp = 1
* Shoe = 2

The freeform sketches done out of the study are all done in the full CASSIE system, with stroke structuring and surface inference, and are given a simple string as name based on what they represent.