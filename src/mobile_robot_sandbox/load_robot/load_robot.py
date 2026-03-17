from compas.scene import SceneObject
from mobile_robot_control.mobile_robot import MobileRobot
from mobile_robot_control.mobile_robot_client import MobileRobotClient

from scriptcontext import sticky as st


def load_robot(ros_client, load, prefix, key='robot_AA'):
    if ros_client and ros_client.is_connected and load:
        # Load URDF from ROS
        robot = ros_client.load_robot(
                load_geometry=True,
                urdf_param_name='{}/robot_description'.format(prefix),
                srdf_param_name='{}/robot_description_semantic'.format(prefix))
        robot.scene_object = SceneObject(item=robot.model)
        mobile_robot = MobileRobot(robot.model, robot.scene_object, robot.semantics, client=None)
        st[key] = mobile_robot

    mobile_robot = st.get(key, None)
    if mobile_robot:  # client sometimes need to be restarted, without needing to reload geometry
        mobile_robot.mobile_client = MobileRobotClient(ros_client)
        mobile_robot.client = ros_client

    return mobile_robot