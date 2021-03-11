# Sketch history data

Each file contains a record of all strokes sketched during the session, along with creation/deletion time (if deleted), and both the raw input samples captured from the controller position and the structured result outputed by CASSIE (in the form of a poly-Bézier or line).

## JSON format

Each files contains a list of stroke objects, each stroke object being described by the following scheme:

```json
{
  // Unique ID
	id: i,
  // A list of N 3D input points captured for this stroke
	input_samples: [ [x, y, z], ...],
  // Type of the curve described by the control points
  curve_type: 'polybezier' | 'line',
  // A list of the control points describing the fitted curve (either a line or a cubic polybézier)
  ctrl_pts: [
            	[[x0, y0, z0], [x1, y1, z1], [x2, y2, z2], [x0, y0, z0]], // ctrl pts for 1 cubic bezier
  						[ ... ]
						],
	// Time of creation of this stroke
	creation_time: t,
	// Time of deletion of this stroke (or null if it wasn't deleted)
	deletion_time: t | None
}
```

## Remarks

* Time is stored as an absolute value relative to some arbitrary origin, it does not necessarily start at 0 at beginning of sketch
* The control points refer to the neatened curve obtained from the input samples by our system. In case of the *Freehand* system (files `xx-0-x.json`), this corresponds to simple line/polybézier fitting. In case of the other 2 systems, this corresponds to the neatened curve, taking into account potential intersection and beautification constraints.
* We store cubic polybéziers as a list of Béziers segments (4 ctrl pts each), and lines as a list of line segments (2 ctrl pts each), although in practice we only have simple lines and no polylines.