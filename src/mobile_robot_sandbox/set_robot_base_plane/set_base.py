from compas.geometry import Frame
from compas_rhino.conversions import frame_to_rhino_plane

def set_base(robot, use_rhino_worldXY=True, custom_plane=None):
    if use_rhino_worldXY:
        base_frame = Frame.worldXY()
    else:
        if custom_plane is None:
            raise ValueError('custom_plane is required when use_rhino_worldXY is False')
        base_frame = Frame(custom_plane.Origin, custom_plane.XAxis, custom_plane.YAxis)

    # Base_frame is BCF in WCF
    if robot:
        robot.BCF = base_frame
        print(robot.BCF)

    base_plane = frame_to_rhino_plane(base_frame)
    arm_base_plane = frame_to_rhino_plane(robot.RCF) if robot else None

    return base_frame, base_plane, arm_base_plane