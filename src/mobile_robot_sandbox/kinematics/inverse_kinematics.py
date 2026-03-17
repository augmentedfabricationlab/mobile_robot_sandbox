import math
from compas.geometry import Frame, Transformation
from compas_robots import Configuration
from ur_fabrication_control.kinematics.ur_kinematics import (
    inverse_kinematics as ur_inverse_kinematics,
)
from ur_fabrication_control.kinematics.ur_params import ur_params as ur_parameters
from compas_rhino.conversions import plane_to_compas_frame
from compas_ghpython.drawing import draw_frame
from roslibpy import tf


def inverse_kinematics(robot, plane_WCS, lift, idx=0):
    if not robot:
        return None, None, None, []

    frame_WCS = plane_to_compas_frame(plane_WCS)

    tf_client = tf.TFClient(
        robot.mobile_client.ros_client,
        fixed_frame="robot_base_footprint",
        angular_threshold=0.0,
        rate=10.0,
    )
    tf_client.subscribe("robot_arm_base", robot._receive_base_frame_callback)

    # transform frame to robot coordinate system
    print(robot.RCF)
    T1 = Transformation.from_frame_to_frame(
        robot.RCF.translated([0, 0, lift]), Frame.worldXY()
    )
    T2 = Transformation.from_frame_to_frame(robot.BCF, Frame.worldXY())

    frame_RCS = frame_WCS.transformed(T1 * T2)

    print(frame_RCS)
    if robot.attached_tool:
        tool0_RCS = robot.from_tcf_to_t0cf([frame_RCS])[0]
    else:
        tool0_RCS = frame_RCS

    plane_tool0_RCS = draw_frame(tool0_RCS)
    plane_RCS = draw_frame(frame_RCS)

    # calculate solutions to frame
    params = ur_parameters["ur20"]
    solutions = ur_inverse_kinematics(tool0_RCS, params)

    if not len(solutions):
        joint_values = [0, 0, 0, 0, 0, 0]
        configuration = Configuration.from_prismatic_and_revolute_values(
            [robot.lift_height], joint_values
        )
    else:
        joint_values = solutions[idx]
        # rotation fix
        joint_values[1] -= 2 * math.pi
        configuration = Configuration.from_prismatic_and_revolute_values(
            [robot.lift_height], joint_values
        )

    print(configuration)
    return configuration, plane_tool0_RCS, plane_RCS, solutions
