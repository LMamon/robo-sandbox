import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = get_package_share_directory('rxsim')
    mode = LaunchConfiguration('mode')

    return LaunchDescription([
        DeclareLaunchArgument('mode', 
                            default_value='viz', 
                            description='Mode to launch: viz or autopilot'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_share, 'launch', 'viz.launch.py')
            ),
            condition=LaunchConfigurationEquals('mode', 'viz')
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_share, 'launch', 'autopilot.launch.py')
            ),
            condition=LaunchConfigurationEquals('mode', 'autopilot')
            )
        ])