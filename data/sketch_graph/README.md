# Sketch graph data

Each file contains a lists of strokes, graph segments and graph nodes that describe the connectivity structure of the sketch. This is only available for structured sketches, done in *Armature* and *Patch* systems.

The sketch graph data represents the final state of the sketch, contrary to the sketch history which represents the evolution of a sketch. A stroke is composed of one or multiple segments, and segments have 2 endpoint nodes. Multiple segments may meet at a node.

This data can be used to test algorithms for automatic cycle detection on curve networks. However, please note that curve networks may have some erroneous connectivity, due to minor misses of our structuring method. Furthermore, we did not instruct participants to take specific care to draw well-connected networks, and some of them did not - especially in *Armature* mode.

Because of a lack of data export features at the time of the user study and generation of most of the results in the paper, we did not export the curve network data from the application, and instead did a post-processing procedure where we tried to recover the curve network data by detecting intersections in the sketch. This was done in a hurry and pretty poorly, so our networks may have some errors such as missing connectivity at some nodes or overly-connected parts, in very dense zones.

You can generate your own curve network data by sketching using our [VR Unity application](https://gitlab.inria.fr/D3/cassie). The export feature has been implemented so your exported curve network will match exactlty the connectivity of your sketch.



## Examples of use

* [Python script that displays the curve network for a sketch](../../scripts/example_sketch_graph.py)

## JSON format

Each files contains a JSON object described by the following scheme:

```js
{
  // All strokes present at the end of the sketch
  strokes: [
    {
      // Stroke ID
      id: i,
      // IDs of all segments that belong to this stroke
      segments: [ k, ..., l ]
    },
    ...
  ],
  // All segments of the graph
  segments: [
    {
    	// Segment ID
    	id: k,
      // Stroke to which this segment belongs
    	stroke_id: i,
      // Control points of line/polyb??zier for this curve segment
      ctrl_pts: [
                 [[x0, y0, z0], [x1, y1, z1], [x2, y2, z2], [x3, y3, z3]], // ctrl pts for 1 cubic bezier
                 [ ... ]
                ],
      // ID of nodes incident on that segment (2)
      nodes: [ r, s]
    },
    ...
  ],
  // All nodes of the graph
  nodes: [
    {
      // Node ID
      id: r,
      // Node position
      position: [x, y, z],
      // ID of segments incident on that node
      neighbor_edges: [k, ...]
    },
    ...
  ]
}
```

