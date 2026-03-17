from compas_rhino.conversions import frame_to_rhino

import ghpythonlib.components as ghcomp
import Rhino.Geometry as rg

def visualize(
    robot,
    configuration,
    show_frames=False,
    show_base_frame=False,
    show_end_effector_frame=False,
    show_visual_meshes=False,
    show_collision_meshes=False,
    show_attached_collision_meshes=False,
):
    if not robot or not configuration:
        return None, None, None, None, None, None

    joint_planes = None
    base_plane = None
    end_effector_plane = None
    visual_meshes = None
    collision_meshes = None
    attached_collision_meshes = None

    robot.update(configuration)
    bcf_plane = frame_to_rhino(robot.BCF)

    if show_frames:
        joint_frames = robot.model.transformed_frames(configuration)
        joint_planes = [frame_to_rhino(frame) for frame in joint_frames]
        joint_planes = ghcomp.Orient(joint_planes, rg.Plane.WorldXY, bcf_plane)[0]

    if show_base_frame:
        base_frame = robot.model.forward_kinematics(configuration, robot.model.get_base_link_name())
        base_plane = frame_to_rhino(base_frame)
        base_plane = ghcomp.Orient(base_plane, rg.Plane.WorldXY, bcf_plane)[0]

    if show_end_effector_frame:
        tool0_frame = robot.model.forward_kinematics(configuration, "robot_arm_tool0")
        end_effector_frame = robot.from_t0cf_to_tcf([tool0_frame])[0]
        end_effector_plane = frame_to_rhino(end_effector_frame)
        end_effector_plane = ghcomp.Orient(end_effector_plane, rg.Plane.WorldXY, bcf_plane)[0]

    if show_visual_meshes:
        visual_meshes = robot.draw_visual()
        visual_meshes = ghcomp.Orient(visual_meshes, rg.Plane.WorldXY, bcf_plane)[0]

    if show_collision_meshes:
        collision_meshes = robot.draw_collision()
        collision_meshes = ghcomp.Orient(collision_meshes, rg.Plane.WorldXY, bcf_plane)[0]

    if show_attached_collision_meshes:
        attached_collision_meshes = []

    return (
        joint_planes,
        base_plane,
        end_effector_plane,
        visual_meshes,
        collision_meshes,
        attached_collision_meshes,
    )




