from scriptcontext import sticky as st

from compas_fab.backends import RosClient


def connect_ros(connect, ip='127.0.0.1', port=9090, key='ros_client_001'):
    ros_client = st.get(key, None)

    if ros_client:
        st[key].close()
    if connect:
        st[key] = RosClient(ip, port)
        st[key].run(5)

    ros_client = st.get(key, None)
    is_connected = ros_client.is_connected if ros_client else False

    return ros_client, is_connected

