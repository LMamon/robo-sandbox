import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import LogInfo

def generate_launch_description():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    bridge_yaml = os.path.join(this_dir, 'bridge.yaml')

    uxrce_agent = ExecuteProcess(
        cmd=['MicroXRCEAgent', 'udp4', '-p', '8888'],
        output='screen'
    )
    
    ros_bag = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-a'],
        output='screen'
    )

    bridge_node = Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    name='gz_parameter_bridge',
                    parameters=[{'config_file': bridge_yaml}],
                    output='screen'
                )
    
    ov_launch = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(
                            get_package_share_directory('ov_msckf'),
                            'launch',
                            'subscribe.launch.py'
                        )
                    ),
                    launch_arguments={
                        'config': 'gazebo_px4'
                    }.items()
                )

    vio_node = Node(
                    package='vio',
                    executable='vio_node',
                    name='vio_node',
                    parameters=[{"use_sim_time": True}],
                    output='screen'
                )
    
    foxglove_bridge = Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            output='screen'
        )
        # TODO: add nodes for computervision to start perception stack and publish to ROS topics
        # Node(
        #     package='perception',
        #     executable='perception_node',
        #     name='perception_node',
        #     output='screen'
        # ),
    return LaunchDescription([
        bridge_node,
        TimerAction(
            period=2.0,
            actions=[foxglove_bridge]
        ),
        TimerAction(
            period=3.0,
            actions=[ros_bag]
        ),
        TimerAction(
            period=4.0,
            actions=[vio_node]
        ),
        TimerAction(
            period=6.0,
            actions=[ov_launch]
        ),
        TimerAction(
            period=8.0,
            actions=[uxrce_agent]
        ),
        TimerAction(
            period=10.0,
            actions=[LogInfo(msg="SYSTEM READY - start PX4 now")]
        )
    ])
