# CASSIE - VR sketch data

This repository contains the dataset from the CASSIE project, both raw data recorded directly from our VR sketching app, along with data that has been reformated and compacted for easier downstream analysis of the sketches. Some example scripts are included to show how the data can be loaded and displayed.

We provide data for:

* 48 sketches done by 12 participants during a controlled user study (the task was to take max 5 minutes to sketch a running shoe or a desk lamp using 3 variants of the CASSIE system)
* 16 sketches done to demonstrate the overall system (the models are varied and the sketches are more complex)

Additionnally, we provide some utility python scripts to load and display the data, which will also support data exported directly from our Unity VR sketching application. See code and binaries [here](https://gitlab.inria.fr/D3/cassie).

More details about the CASSIE project: [webpage](https://ns.inria.fr/d3/CASSIE/), [paper](http://www-sop.inria.fr/reves/Basilic/2021/YASBS21/CASSIE_author_version.pdf).

Explore all the sketches directly in your browser: [CASSIE data website](https://ns.inria.fr/d3/CASSIE/sketch-explorer/).

If this is useful for your research, please [cite us](#citing-this-project).

## About the data

All sketches were collected in our custom VR sketching system, and are not representative of all VR sketching practices in a general context. In particular, the 36 sketches done in *Armature* and *Patch* mode from the study, and the 16 varied sketches were created using specific features from CASSIE that aimed to **help and encourage users to create well-connected curve networks** by sketching. Furthermore, we instructed participants to adopt a **sparse sketching style** in their drawings.

## Data

The data files available are, for each sketch, in 3 sub-folders:

* [`curves`](data/curves#curves-data) : a simple file format where all strokes present in the final sketch are listed as polylines. We give the input/non beautified strokes here.
* [`sketch_history`](data/sketch_history#sketch-history-data) : a list of all strokes sketched during the session, along with creation/deletion time (if deleted), and both the raw input samples captured from the controller position and the structured result outputed by CASSIE (in the form of a poly-B??zier or line).
* [`sketch_graph`](data/sketch_graph#sketch-graph-data) : lists of strokes, graph segments and graph nodes that describe the connectivity structure of the sketch (NB: this is only available for structured sketches, done in *Armature* and *Patch* systems).
* [`raw_data`](data/raw_data#raw-data) : direct export from CASSIE interactive applications, in the form of a full history of actions undertaken by the user during this session, and lists of primitives (strokes and patches) created (NB: the mesh for each patch was not recorded).

For most purposes, the data from `curves` or `sketch_history` folders should contain all necessary data. For example, `sketch_history` files are used to visualize sketching sessions on the [CASSIE data website](https://ns.inria.fr/d3/CASSIE/sketch-explorer/).

Each of the 4 folders has a README detailing the specific schema used for the data.

## Scripts

The folder `scripts` contains python scripts that can be used to load and display sketch data, using either [polyscope](https://github.com/nmwsharp/polyscope) or [pythreejs](https://github.com/jupyter-widgets/pythreejs) widgets in a Jupyter Notebook.

For example, you can try to display a sketch by running *(NB: needs polyscope to run)*:

```bash
> cd scripts

# Display the final hmd sketch (input strokes)
> python3 example_curves_file "hmd_modern.curves"

# Display the hat sketch (input strokes and beautified, with sketched time visualized)
> python3 example_sketch_history.py "hat.json"

# Display the sketch from participant 9, done with the Armature system (1), of the shoe model (2)
> python3 example_sketch_history.py 9 1 2

# Display the curve network from participant 2, done with the Patch system (2), of the shoe model (2)
> python3 example_sketch_graph.py 2 2 2
```

Or launch the jupyter notebook [`Example - sketch history with pythreejs.ipynb`](scripts/Example%20-%20sketch%20history%20with%20pythreejs.ipynb) *(NB: needs pythreejs if you want to run it locally)*.

## File naming convention

In each folder, there is one `json` file per sketch. Sketches from the study and sketches done outside of the study are mixed.

The files from the study follow the naming convention:

`Participant ID - System ID - Model ID .json`

With the following code for the systems:

* *Freehand* = 0
* *Armature* (automatic structuring of the strokes) = 1
* *Patch* (automatic structuring + surface inference) = 2

And for the models:

* Lamp = 1
* Shoe = 2

The sketches done outside of the study are all done in the full CASSIE system, with stroke structuring and surface inference, and are given a simple string as name based on what they represent (eg: `hat.json`).

## Units

* Timestamps are stored as an absolute value relative to some arbitrary origin, it does not necessarily start at 0 at beginning of a given sketch. Time unit is second.
* All coordinates are in scale of 1 unit = 1m (in real life) when the canvas is at default zoom level. All coordinates are stored in `canvas space` which is often different than user's `world space` due to the possibility to grab the canvas and move it around, or scale it up (up to x3 the default scale). This should be what is desired for most usages (sketch appears fixed).


## License

The code and data in this repository is provided under the MIT License.

## Citing this project

```latex
@InProceedings{YASBS21,
  author       = "Yu, Emilie and Arora, Rahul and Stanko, Tibor and B??rentzen, J. Andreas and Singh, Karan and Bousseau, Adrien",
  title        = "CASSIE: Curve and Surface Sketching in Immersive Environments",
  booktitle    = "ACM Conference on Human Factors in Computing Systems (CHI)",
  year         = "2021",
  url          = "http://www-sop.inria.fr/reves/Basilic/2021/YASBS21"
}
```