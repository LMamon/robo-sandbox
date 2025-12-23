import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    bridge_yaml = os.path.expanduser(this_dir, 'bridge.yaml')
    return LaunchDescription([


        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gz_parameter_bridge',
            parameters=[{'config_file': bridge_yaml}],
            output='screen'
        ),
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen'
        ),
    ])