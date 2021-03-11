# Sketch graph data

Each file contains a lists of strokes, graph segments and graph nodes that describe the connectivity structure of the sketch. This is only available for structured sketches, done in *Armature* and *Patch* systems.

This data can be used to test algorithms for automatic cycle detection on curve networks. However, please note that curve networks may have some erroneous connectivity, due to minor misses of our structuring method. Furthermore, we did not instruct participants to take specific care to draw well-connected networks, and some of them did not - especially in *Armature* mode. All "free creations" - bigger sketches done outside of the study (those that have a textual name) - should have mostly correct connectivity.

The sketch graph data represents the final state of the sketch, contrary to the sketch history which represents the evolution of a sketch.

A stroke is composed of one or multiple segments, and segments have 2 endpoint nodes. Multiple segments may meet at a node.

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
      // Control points of line/polybézier for this curve segment
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
    // Node ID
    id: r,
    // Node position
    position: [x, y, z],
    // ID of segments incident on that node
    neighbor_edges: [k, ...]
  ]
}
```

