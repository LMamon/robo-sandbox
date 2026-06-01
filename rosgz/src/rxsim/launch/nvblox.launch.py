from launch_ros.descriptions import ComposableNode
from launch_ros.actions import ComposableNodeContainer
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    rxsim_config = os.path.join(
        get_package_share_directory('rxsim'),
        'config/nvblox/3d_reconstruction.yaml'
    )

    nvblox_node = ComposableNode(
        name='nvblox_node',
        package='nvblox_ros',
        plugin='nvblox::NvbloxNode',
        remappings=[
            ('camera_0/depth/image', '/px4vision/depth/image'),
            ('camera_0/depth/camera_info', '/px4vision/depth/camera_info'),
            ('camera_0/color/image', '/stereo/left'),
            ('camera_0/color/camera_info', '/stereo/left/camera_info'),
        ],

        parameters=[
            rxsim_config
        ]
    )

    container = ComposableNodeContainer(
        name='nvblox_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[nvblox_node],
        output='screen',
    )

    return LaunchDescription([
        container
    ])