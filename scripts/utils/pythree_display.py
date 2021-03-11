import pythreejs as three
import matplotlib.colors as mcolors
from utils.curves import *

# NB: this dependency is only used for vector display functions (pythree_vectors function)
# Typically, it is not used in the Example Jupyter notebook
try:
    from scipy.spatial.transform import Rotation as R
except ImportError:
    print("scipy.spatial.transform is not available")

view_width = 600
view_height = 400

colors_list = list(mcolors.TABLEAU_COLORS.values())

##### Base rendering function
# Pass it a list of pythree objects, they get added to an empty scene and rendered
# The scene contains only some axes and an ambient light
def render_with_pythree(geometry_to_draw):
    camera = three.PerspectiveCamera(
        position=[2, 3, 0], aspect=view_width/view_height)
    light = three.AmbientLight(intensity=2)
    axes = three.AxesHelper(size=10)
    # key_light = three.DirectionalLight(color='white', position=[3, 5, 1], intensity=0.5)

    scene_children = [camera, light, axes] + geometry_to_draw

    scene = three.Scene(children=scene_children)
    renderer = three.Renderer(camera=camera, scene=scene,
                              controls=[three.OrbitControls(
                                  controlling=camera)],
                              width=view_width, height=view_height)
    display(renderer)

##### Geometry creation helper functions

# Creates a list of pythree geometry for a list of polylines
def pythree_polylines(polylines, colors = None):
    geometry = []

    if colors is None:
        colors = colors_list
    elif len(colors) == 1:
        colors = [colors[0]] * len(polylines)

    for i, samples_list in enumerate(polylines):

        points = np.array([samples_list], dtype="float32").reshape((-1,1,3))
        segments = np.append(points[:-1], points[1:], axis = 1)

        g = three.LineSegmentsGeometry(
            positions=segments
        )
        m = three.LineMaterial(linewidth=5, color=colors[i % len(colors)])
        three_line = three.LineSegments2(g, m)

        geometry.append(three_line)

    return geometry

# Creates a list of pythree geometry for a list of curves (lines or cubic bezier curves)
def pythree_curves(curves, draw_ctrl_pts = False, colors = None, samples_by_bezier = 30):
    geometry = []
    theta = np.linspace(0, 1, samples_by_bezier)

    if colors is None:
        colors = colors_list
    elif len(colors) == 1:
        colors = [colors[0]] * len(curves)

    for i, poly in enumerate(curves):
        if curve_is_line(poly):
            pts_list = []
            for i in range(len(poly)):
                pts_list.append(np.array(poly[i], dtype="float32"))
                segments = np.array(pts_list)
        else:
            # Prepare arrays x, y, z
            x, y, z = poly_bezier(theta, poly)
            polyline = np.array([[x, y, z]], dtype="float32").T.reshape((-1, 1, 3))
            segments = np.append(polyline[:-1], polyline[1:], axis = 1)

        g = three.LineSegmentsGeometry(
            positions=segments
        )
        m = three.LineMaterial(linewidth=5, color=colors[i % len(colors)])
        three_line = three.LineSegments2(g, m)

        geometry.append(three_line)

        if draw_ctrl_pts:
            point_radius = 0.01
            for j, ctrl_pts in enumerate(poly):
                for pt in ctrl_pts:
                    sphere = three.Mesh(
                        three.SphereBufferGeometry(point_radius, 32, 16),
                        #                     three.MeshStandardMaterial(color=mcolors.rgb2hex(mcolors.BASE_COLORS[pts_colors[i]])),
                        three.MeshStandardMaterial(color=colors[i % len(colors)]),
                        position=pt.tolist()
                    )
                    geometry.append(sphere)  
    return geometry

# Creates geometry for a list of vectors
def skew(x):
    return np.array([[0, -x[2], x[1]],
                     [x[2], 0, -x[0]],
                     [-x[1], x[0], 0]])

def rotation(from_vec, to_vec):
    v = np.cross(from_vec, to_vec)
    s = np.linalg.norm(v)
    c = np.dot(from_vec, to_vec)
    vX = skew(v)
    R_mat = np.eye(3,3) + vX + vX @ vX / (1 + c)
    return R.from_matrix(R_mat).as_quat()

def pythree_vectors(directions, origins, colors = None, length = 1):
    geometry = []
    if colors is None:
        colors = colors_list
    elif len(colors) == 1:
        colors = [colors[0]] * len(directions)

    for i, (vec, pos) in enumerate(zip(directions, origins)):
        a = pos
        vec = vec / np.linalg.norm(vec)
        b = pos + vec * length
        
        # Line
        g = three.LineGeometry(
            positions= np.array([a, b], dtype="float32")
        )
        m = three.LineMaterial(linewidth=5, color=colors[i % len(colors)])
        three_line = three.LineSegments2(g, m)
        geometry.append(three_line)
        
        # Arrow head
        # Skip if scipy Rotation is not available
        try:
            three_arrow = three.Mesh(
                three.ConeGeometry(radius = 0.05, height = 0.1),
                three.MeshStandardMaterial(color=colors[i % len(colors)]),
                position = tuple(b),
                quaternion = tuple(rotation(np.array([0,1,0]), vec))
            )
            
            geometry.append(three_arrow)
        except NameError:
            print("Warning: scipy.spatial.transform is not available, vector arrows will not be displayed")

    return geometry

# Creates geometry from a list of points
def pythree_points(points, colors = None, radius = 0.05):
    geometry = []
    if colors is None:
        colors = colors_list
    elif len(colors) == 1:
        colors = [colors[0]] * len(points)
    for i, pt in enumerate(points):
        sphere = three.Mesh(
                        three.SphereBufferGeometry(radius, 16, 16),
                        three.MeshStandardMaterial(color=colors[i % len(colors)]),
                        position=tuple(pt)
                    )
        geometry.append(sphere) 
    return geometry

# Creates geometry for a mesh
def pythree_mesh(vertices, faces, color = None, wireframe=True):
    geometry = []
    if color is None:
        color = colors_list[0]

    mesh_attributes=dict(
        position = three.BufferAttribute(np.asarray(vertices, dtype=np.float32), normalized=False),
        index =    three.BufferAttribute(np.asarray(faces, dtype=np.uint32), normalized=False)
    )
    mesh_geom = three.BufferGeometry(attributes=mesh_attributes) # TODO: generate the vertex normals in order to shade the mesh (shading doesn't work now)
    mesh_obj = three.Mesh(geometry=mesh_geom, material=three.MeshBasicMaterial(color=color, wireframe=wireframe, side='DoubleSide'))

    geometry.append(mesh_obj)
    return geometry
    


##### DRAW API

# Functions to draw a list of strokes, as polylines or curves

def draw_strokes_samples(polylines, colors=None):
    geometry_list = pythree_polylines(polylines, colors)
    render_with_pythree(geometry_list)

    
def draw_curves(curves, colors=None, draw_ctrl_pts=False):
    n_samples = 30 # number of samples by bezier curve
    geometry_list = pythree_curves(curves, draw_ctrl_pts, colors, n_samples)   
    render_with_pythree(geometry_list)
    