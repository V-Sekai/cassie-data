import polyscope as ps
from utils.curves import *

def add_edge_indices_for_stroke(indices, node_count):
    N = node_count - 1
    start_idx = 0
    if len(indices) > 0:
        start_idx = indices[-1, -1] + 1
    left = np.arange(start_idx, start_idx + N).reshape(-1,1)
    right = np.arange(start_idx + 1, start_idx + 1 + N).reshape(-1,1)
    return np.append(indices, np.concatenate((left, right), axis = 1), axis = 0)

def get_edges_for_strokes(polylines):
    edges = np.empty((0,2))

    for poly in polylines:
        edges = add_edge_indices_for_stroke(edges, len(poly))

    return edges.astype(int)


def polyscope_draw_all_sketch(sketch_history, draw_structured = True, skip_deleted = True):

    N_samples = 40 # nb of samples for the poly-beziers

    ps.init()

    # Raw curves
    nodes_input = np.empty((0,3))
    edges_input = np.empty((0,2))

    if draw_structured:
        # Final curves
        nodes_structured = np.empty((0,3))
        edges_structured = np.empty((0,2))

    # Additional per stroke info vectors
    creation_times = np.empty(0)
    stroke_ids = np.empty(0)
    if not skip_deleted:
        deletion_times = np.empty(0)

    for stroke in sketch_history:
        # Skip deleted strokes
        if skip_deleted and (stroke["deletion_time"] is not None):
            continue

        ctrl_pts = stroke["ctrl_pts"]

        input_samples = stroke["input_samples"]

        stroke_id = stroke["id"]

        creation_time = stroke["creation_time"]

        # Add input samples nodes
        nodes_input = np.append(nodes_input, np.array(input_samples), axis = 0)

        # Generate edge indices
        edges_input = add_edge_indices_for_stroke(edges_input, len(input_samples))

        # Store additional info as per-node data (to display in polyscope)
        creation_times = np.append(creation_times, creation_time * np.ones(len(input_samples)))
        stroke_ids = np.append(stroke_ids, stroke_id * np.ones(len(input_samples)))

        if not skip_deleted:
            deletion_time = 10e6 if stroke["deletion_time"] is None else stroke["deletion_time"]
            deletion_times = np.append(deletion_times, deletion_time * np.ones(len(input_samples)))

        # Structured strokes
        if draw_structured:

            node_count = 0

            # Add final curve nodes
            if curve_is_line(ctrl_pts):
                # is line
                nodes_line = []
                for edge in ctrl_pts:
                    nodes_line.append(np.array(edge[0]))
                nodes_line.append(ctrl_pts[-1][1])

                node_count = len(nodes_line)

                nodes_structured = np.append(nodes_structured, np.array(nodes_line), axis = 0)
                
            else:
                theta = np.linspace(0, 1, N_samples)
                x, y, z = poly_bezier(theta, ctrl_pts)
                nodes_bezier = np.array([x, y, z]).T
                node_count = len(nodes_bezier)
                nodes_structured = np.append(nodes_structured, nodes_bezier, axis = 0)

            # Generate edge indices
            edges_structured = add_edge_indices_for_stroke(edges_structured, node_count)


    ps_net_input = ps.register_curve_network("Input strokes", nodes_input, edges_input, material="clay", radius=0.0035)

    if draw_structured:
        ps_net_structured = ps.register_curve_network("Structured strokes", nodes_structured, edges_structured, material="clay", radius=0.0035)

    # Add info on strokes
    ps_net_input.add_scalar_quantity("Creation time", creation_times, defined_on='nodes', enabled=False, cmap='blues')
    ps_net_input.add_scalar_quantity("Stroke ID", stroke_ids, defined_on='nodes', enabled=False, cmap='viridis')
    if not skip_deleted:
        ps_net_input.add_scalar_quantity("Deletion time", deletion_times, defined_on='nodes', enabled=False, cmap='reds')

    ps.show()
