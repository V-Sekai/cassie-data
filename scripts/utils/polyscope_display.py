import polyscope as ps
from utils.curves import *
from utils.load import parse_ctrl_pts, parse_vec3

def add_edge_indices_for_stroke(indices, node_count):
    N = node_count - 1
    start_idx = 0
    if len(indices) > 0:
        start_idx = indices[-1, -1] + 1
    left = np.arange(start_idx, start_idx + N).reshape(-1,1)
    right = left + 1
    return np.append(indices, np.concatenate((left, right), axis = 1), axis = 0)

def get_edges_for_strokes(polylines):
    edges = np.empty((0,2))

    for poly in polylines:
        edges = add_edge_indices_for_stroke(edges, len(poly))

    return edges.astype(int)


def polyscope_draw_all_sketch(sketch_history, draw_structured = True, skip_deleted = True):

    N_samples = 40 # nb of samples for the poly-beziers

    # Careful: call this only once in a script!
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

            # Add final curve pts
            pts = np.empty((0,3))
            if curve_is_line(ctrl_pts):
                for edge in ctrl_pts:
                    pts = np.row_stack([pts, np.array(edge[0])])
                pts = np.row_stack([pts, np.array(ctrl_pts[-1][1])])
                
            else:
                theta = np.linspace(0, 1, N_samples)
                x, y, z = poly_bezier(theta, ctrl_pts)
                pts = np.array([x, y, z]).T

            node_count = len(pts)
            nodes_structured = np.append(nodes_structured, pts, axis = 0)

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


def polyscope_draw_sketch_graph(sketch_graph):
    N_samples = 30 # nb of samples for the poly-beziers

    # Careful: call this only once in a script!
    ps.init()

    segments_data = sketch_graph["segments"]
    nodes_data = sketch_graph["nodes"]

    # Nb of incident segments per node
    neighbors_counts = [np.array(len(node["neighbor_edges"])) for node in nodes_data]
    max_neighbors = max(neighbors_counts)

    # Register nodes
    ps_nodes = ps.register_point_cloud("Nodes", np.array([np.array(parse_vec3(node["position"])) for node in nodes_data]), radius=0.01)
    ps_nodes.add_scalar_quantity("Neighbors", np.array(neighbors_counts), enabled=True, vminmax=(1,max_neighbors), cmap="reds")

    # Form polylines
    polylines = []
    stroke_ids = []
    for s in segments_data:
        ctrl_pts = parse_ctrl_pts(s["ctrl_pts"])
        pts = np.empty((0,3))
        if curve_is_line(ctrl_pts):
            for edge in ctrl_pts:
                pts = np.row_stack([pts, np.array(edge[0])])
            pts = np.row_stack([pts, np.array(ctrl_pts[-1][1])])
            
        else:
            theta = np.linspace(0, 1, N_samples)
            x, y, z = poly_bezier(theta, ctrl_pts)
            pts = np.array([x, y, z]).T

        polylines.append(pts)
        stroke_ids += [s["stroke_id"]] * len(pts)

    all_segment_pts = np.row_stack(polylines)
    all_segment_edges = get_edges_for_strokes(polylines)

    ps_curve_net = ps.register_curve_network("Sketch curve network", all_segment_pts, all_segment_edges)
    ps_curve_net.add_scalar_quantity("Stroke ID", np.array(stroke_ids), defined_on="nodes")

    ps.show()


def polyscope_draw_polylines(polylines):
    # Careful: call this only once in a script!
    ps.init()

    pts = np.empty((0,3))
    edges = np.empty((0,2))

    for polyline in polylines:
        pts = np.row_stack([pts, np.array(polyline)])
        edges = add_edge_indices_for_stroke(edges, len(polyline))

    ps.register_curve_network("Sketch", pts, edges)

    ps.show()
