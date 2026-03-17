import math

from compas_robots.model import Joint
from compas_robots import Configuration


def forward_kinematics(robot, lift, j1, j2, j3, j4, j5, j6):
    if not robot:
        print("No robot provided for forward kinematics.")
        return None

    robot.lift_height = lift
    joint_positions = [lift, j1, j2, j3, j4, j5, j6]
    print(joint_positions)
    joint_types = robot.model.get_joint_types()[4:11]
    print(joint_types)
    joint_names = robot.model.get_configurable_joint_names()[4:11]
    print(joint_names)

    for i, joint_type in enumerate(joint_types):
        if joint_type == Joint.REVOLUTE:
            joint_positions[i] = math.radians(joint_positions[i])

    configuration = Configuration(joint_positions, joint_types, joint_names)
    print(configuration)
    return configuration
