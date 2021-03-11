# Raw data

Each file is a direct export from CASSIE interactive applications, in the form of a full history of actions undertaken by the user during this session, and lists of primitives (strokes and patches) created.

NB: contrary to stroke geometric data, the mesh data for each patch was not recorded, only creation events and manual deletion events.

> This is most probably not useful data for future usages, and is only provided for completeness. Please check out the processed data formats, such as [`sketch_history`](../sketch_history#sketch-history-data) and [`sketch_graph`](../sketch_graph#sketch-graph-data).

## JSON format

Each files contains a JSON object described by the following scheme:

```js
{
  // Sketching system ID (0 = freehand, 1 = armature, 2 = patch)
  sketchSystem: 0 | 1 | 2,
  // Sketch model (model being used to sketch on: 0 = none, 1 = lamp, 3 = shoe)
  sketchModel: 0 | 1 | 3,
  // Interaction mode (1 = study mode, 2 = free creation mode)
  interactionMode: 1 | 2,
  // A list of all recorded actions during the sketching session
  systemStates: [
    {
      // Interaction type:
      // 0 = Idle, 1 = Add stroke, 2 = Delete stroke, 3 = Add surface, 4 = Delete surface manually, 5 = Transform canvas (grab or zoom)
      interactionType: 0 | 1 | 2 | 3 | 4 | 5,
      // Time of action (s)
      time: t,
      // ID of element (stroke/surface) concerned by action (-1 if no element concerned, eg Idle action)
      elementID: i | -1,
      // Is the mirror feature active?
      mirroring: true | false,
      // User head position (3D vector)
      headPos: { x, y, z },
      // User head rotation (quaternion)
      headRot: { x, y, z, w },
      // User primary hand position (3D vector)
      primaryHandPos: { x, y, z },
      // Canvas position (3D vector)
      canvasPos: { x, y, z },
      // Canvas rotation (quaternion)
      canvasRot: { x, y, z, w },
      // Canvas scale (float between 1 = default scale and 3 = max zoom)
      canvasScale: s
    },
    ...
  ],
  // A list of all stroke primitives created during the sketch
  allSketchedStrokes: [
    {
      // Unique stroke ID
      id: i,
      // Control points of fitted polybézier curve / line segment
      // NB: stroke is a line segment if 2 ctrl pts, otherwise it is a cubic polybézier
      ctrlPts: [ {x0, y0, z0}, {x1, y1, z1}, {x2, y2, z2}, {x3, y3, z3} ],
      // A list of 3D input points captured for this stroke
      inputSamples: [ [x, y, z], ...],
      // Position constraints applied by the structuring algorithm
      appliedPositionConstraints: [ {}, ... ],
      // Position constraints rejected by the structuring algorithm
      rejectedPositionConstraints: [ {}, ... ],
                                    
    },
    ...
  ],
  // A list recording all surface patches created during the sketch
  allCreatedPatches: [
    {
      // Unique patch ID
      id: i,
      // Whether it was created by the automatic detection algorithm (true) or manually added by the user (false)
      foundByAlgo: true | false,
      // ID of the strokes that border parts of this surface
      strokesID: [ ... ]
    }
  ]
}
```

## Remarks

* Since this data is straight out from the Unity application, some minor aspects of the data are not uniform across files because of minor changes to the application done at some point in time, to accomodate for more precise data gathering. The main change is on the format of `appliedPositionConstraints` and `rejectedPositionConstraints` which sometimes contain only a 3D vector, and sometimes contain more data. Those were specific to our user study and shouldn't be very useful for general usage.
* The control points refer to the neatened curve obtained from the input samples by our system. In case of the *Freehand* system (files `xx-0-x.json`), this corresponds to simple line/polybézier fitting. In case of the other 2 systems, this corresponds to the neatened curve, taking into account potential intersection and beautification constraints.
* We store both lines and cubic polybéziers as a flat list of control points (eg a polybézier with 2 segments would have 2 * 4 - 1 = 7 ctrl pts).
* All vectors are stored as objects with `x, y, z` properties.
* We only store manual patch deletion event, while there are also automatic patch deletion events happening (the surface inference algorithm automaticall creates and deletes patches).