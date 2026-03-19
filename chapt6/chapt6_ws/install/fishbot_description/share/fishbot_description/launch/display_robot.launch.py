import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # 获取默认urdf路径
    urdf_package_path = get_package_share_directory('fishbot_description')
    urdf_path = os.path.join(urdf_package_path, 'urdf', 'first_robot.urdf')
    default_rviz_config_path = os.path.join(urdf_package_path, 'config', 'default_robot_model.rviz')
    
    # 声明一个urdf目录参数，方便修改
    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(urdf_path),description='The urdf file path'
    )
    #通过文件路径，获取内容，并转换成参数值对象，以供传入robot_state_publisher节点
    substitutions_command_result = launch.substitutions.Command(['cat ', launch.substitutions.LaunchConfiguration('model')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result, value_type=str)
    
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_value}]
    )
    
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )
    
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
        )
    
    return launch.LaunchDescription([
        action_declare_arg_model_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])