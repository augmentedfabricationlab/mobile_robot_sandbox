'''Attach tool to robot end effector'''
import os
from compas.geometry import Frame, Vector
from compas.datastructures import Mesh
from compas_rhino.conversions import mesh_to_rhino
from compas_fab.robots import Tool

from mobile_robot_control.multitool import MultiTool
from compas_ghpython.drawing import draw_frame


# Package-relative data directory: <module>/data/tool_geometry
_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


def attach_tool(tool_id, robot=None, attach=False, remove=False, update=False, data_path=None, show=False):
    if data_path is None:
        data_path = _DATA_DIR
        print("Using package-relative data from: {}".format(data_path))
    filename_collision = None
    multitool = False
    visuals = None
    collision = None

    if tool_id == 0:
        filename_visuals = 'measurement_tool.stl'
        ee_frame = Frame([0, 0, 0.109], [1, 0, 0], [0, 1, 0])
        tool_name = 'pin'

    elif tool_id == 1:  # measurement-tool-tip-dc-ps
        filename_visuals = 'measurement_toolx3.stl'
        tool_name = 'pin_x3'
        filename_collision = 'abele/split_90deg/250213_90deg_adapter.stl'

        pin_frame = Frame([0.000, 0.000, 0.29642], [1, 0, 0], [0, 1, 0])
        camera_frame = Frame([0.039977881576833754, 0.0818447722840289, 0.1611195120832291], [1, 0, 0], [0, 1, 0])
        scanner_frame = Frame([-0.0167, 0.0431, 0.3908], [1, 0, 0], [0, 1, 0])

        tool_frames = {"pin_x3": pin_frame, "camera": camera_frame, "scanner": scanner_frame}
        ee_frame = tool_frames["pin_x3"]
        multitool = True

    elif tool_id == 2:  # marker tracking camera with field of View (FOV)
        filename_visuals = 'marker_tracking/extruder_marker_tracking_FOV.stl'
        tool_name = 'camera_FOV'
        filename_collision = 'marker_tracking/extruder_marker_tracking_FOV.stl'
        tool_centerpoint = (-0.000384, -0.292214, 0.312472)
        tool_orientation_x = (0.009997, 0, 0)
        tool_orientation_y = (0, 0.009396, -0.003416)
        ee_frame = Frame(tool_centerpoint, tool_orientation_x, tool_orientation_y)

    elif tool_id == 3:  # marker tracking camera without FOV
        filename_visuals = 'marker_tracking/extruder_marker_tracking.stl'
        tool_name = 'camera'
        filename_collision = 'marker_tracking/extruder_marker_tracking.stl'
        tool_centerpoint = (-0.000384, -0.292214, 0.312472)
        tool_orientation_x = (-0.009997, 0, 0)
        tool_orientation_y = (0, 0.009396, -0.003416)
        ee_frame = Frame(tool_centerpoint, tool_orientation_x, tool_orientation_y)

    elif tool_id == 5:
        filename_visuals = 'concrete_extruder_v1_10mm_0deg.stl'
        tool_name = '2K_extruder_straight'
        filename_collision = 'concrete_extruder_v1_10mm_0deg_collision.stl'
        tool_centerpoint = (0, -0.154355, 0.361564)
        tool_orientation_x = (0, -0.149169, 0.367692)
        tool_orientation_y = (1, 0.0, 0.0)
        vec = Vector.from_start_end(tool_centerpoint, tool_orientation_x)
        ee_frame = Frame(tool_centerpoint, tool_orientation_y, vec)

    elif tool_id == 6:
        filename_visuals = 'earth_extruder_v1_short.stl'
        tool_name = 'earth_extruder'
        filename_collision = 'earth_extruder_v1_10mm_15deg_collision_simple_short.stl'
        tool_centerpoint = (-1.88102e-09, -0.404208, 0.133956)
        tool_orientation_x = (-1.46958e-18, -0.404208, 0.139956)
        tool_orientation_y = (1, 0, 0)
        vec = Vector.from_start_end(tool_centerpoint, tool_orientation_x)
        ee_frame = Frame(tool_centerpoint, tool_orientation_y, vec)

    elif tool_id == 7:
        filename_visuals = 'abele/250515_0deg_adapter_straight_inlet.stl'
        tool_name = '2K_extruder_0deg'
        filename_collision = 'abele/250515_0deg_adapter_straight_inlet.stl'
        tool_centerpoint = (0.00302, -0.29571, 0.40445)
        tool_orientation_x = (0.0366, 0, 0)
        tool_orientation_y = (0, 0.0051, 0.0141)
        ee_frame = Frame(tool_centerpoint, tool_orientation_x, tool_orientation_y)

    elif tool_id == 8:  # abele
        filename_visuals = 'abele/split_90deg/250213_90deg_adapter_straight_inlet.stl'
        tool_name = '2K_extruder_90deg'
        filename_collision = 'abele/split_90deg/250213_90deg_adapter_straight_inlet.stl'
        tool_centerpoint = (0.000, -0.29786, 0.361)
        tool_orientation_x = (0.0151, 0, 0)
        tool_orientation_y = (0, -0.014, 0.0056)
        ee_frame = Frame(tool_centerpoint, tool_orientation_x, tool_orientation_y)

    elif tool_id == 9:  # measurement-tool-abele-tip
        filename_visuals = 'abele/split_90deg/250213_90deg_adapter.stl'
        tool_name = '2K_measurement_tip'
        filename_collision = 'abele/split_90deg/250213_90deg_adapter.stl'
        tool_centerpoint = (0, -0.30709, 0.36211)
        tool_orientation_x = (0.0781, 0, 0)
        tool_orientation_y = (0, -0.0298, 0.0127)
        ee_frame = Frame(tool_centerpoint, tool_orientation_x, tool_orientation_y)

    else:
        raise ValueError("Unknown tool_id: {}".format(tool_id))

    tool_geometry_path = os.path.join(data_path, 'tool_geometry')
    ee_mesh = Mesh.from_stl(os.path.join(tool_geometry_path, filename_visuals))

    if filename_collision is not None:
        collision_mesh = Mesh.from_stl(os.path.join(tool_geometry_path, filename_collision))
        if multitool:
            tool_obj = MultiTool(ee_mesh, tool_frames, primary_tool_name=list(tool_frames.keys())[0], collision=collision_mesh)
        else:
            tool_obj = Tool(ee_mesh, ee_frame, collision_mesh)
        if show:
            collision = mesh_to_rhino(collision_mesh)
    else:
        if multitool:
            tool_obj = MultiTool(ee_mesh, tool_frames, primary_tool_name=list(tool_frames.keys())[0])
        else:
            tool_obj = Tool(ee_mesh, ee_frame)

    if show:
        visuals = mesh_to_rhino(ee_mesh)

    ee_plane = draw_frame(ee_frame)
    print(ee_frame.quaternion.xyzw)

    if robot:
        if attach:
            robot.attach_tool(tool_obj)
        if remove:
            robot.detach_tool()
        if update:
            robot.attached_tool.set_active_tool_frame(tool_name)

    return tool_obj, ee_plane, visuals, collision

# Todo: Cleanup the attach_tool.py and corresponting geometry in the data folder.
# Todo: find a better way to import the tool geometry so we dont mix up the code with the data. Config file with path to geometry?
