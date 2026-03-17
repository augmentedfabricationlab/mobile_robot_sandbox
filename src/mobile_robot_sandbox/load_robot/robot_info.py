def robot_info(robot):
    if robot:
        robot.info()
        return robot.main_group_name
    return None
