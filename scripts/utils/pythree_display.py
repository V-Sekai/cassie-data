import pythreejs as three
import matplotlib.colors as mcolors
from utils.curves import *

view_width = 600
view_height = 400

colors_list = list(mcolors.TABLEAU_COLORS.values())


def render_with_pythree(geometry_to_draw):
    camera = three.PerspectiveCamera(
        position=[2, 3, 0], aspect=view_width/view_height)
    light = three.AmbientLight(intensity=1)
    axes = three.AxesHelper(size=10)

    scene_children = [camera, light, axes] + geometry_to_draw

    scene = three.Scene(children=scene_children)
    renderer = three.Renderer(camera=camera, scene=scene,
                              controls=[three.OrbitControls(
                                  controlling=camera)],
                              width=view_width, height=view_height)
    display(renderer)



def draw_strokes_samples(samples_by_stroke, colors=None):
    geometry_list = []

    if colors is None:
        colors = colors_list

    for i, samples_list in enumerate(samples_by_stroke):

        points = np.array([samples_list], dtype="float32").reshape((-1,1,3))
        segments = np.append(points[:-1], points[1:], axis = 1)

        g = three.LineSegmentsGeometry(
            positions=segments
        )
        m = three.LineMaterial(linewidth=5, color=colors[i % len(colors)])
        three_line = three.LineSegments2(g, m)

        geometry_list.append(three_line)


    render_with_pythree(geometry_list)

    

def draw_curves(curves, colors=None, draw_ctrl_pts=False):
    geometry_list = []
    theta = np.linspace(0, 1, 30)

    if colors is None:
        colors = colors_list

    for i, poly in enumerate(curves):
        if curve_is_line(poly):
            pts_list = []
            for i in range(len(poly)):
                pts_list.append(np.array(poly[i], dtype="float32"))
                # pts_list.append(np.array([np.array(poly[i][0]), np.array(poly[i][1])]))
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

        geometry_list.append(three_line)

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
                    geometry_list.append(sphere)

    render_with_pythree(geometry_list)
    