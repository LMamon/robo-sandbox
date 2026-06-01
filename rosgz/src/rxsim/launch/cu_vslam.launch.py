import launch
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    """Launch file which brings up visual slam node configured for Isaac Sim."""
    visual_slam_node = ComposableNode(
        name='visual_slam_node',
        package='isaac_ros_visual_slam',
        plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
        remappings=[('/visual_slam/image_0', '/stereo/left'),
                ('/visual_slam/camera_info_0', '/stereo/left/camera_info'),
                ('/visual_slam/image_1', '/stereo/right'),
                ('/visual_slam/camera_info_1', '/stereo/right/camera_info'),
                ('visual_slam/imu', '/px4vision/imu')
            ],
        parameters=[{
            'use_sim_time': True,
            'enable_image_denoising': False,
            'rectified_images': True,
            'enable_slam_visualization': True,
            'enable_observations_view': True,
            'enable_landmarks_view': False,
            'enable_imu_fusion': True,
            'imu_frame': 'base_link',
            'sync_matching_threshold_ms': 20.0,
            'calibration_frequency': 200.0,
        }])

    visual_slam_launch_container = ComposableNodeContainer(
        name='visual_slam_launch_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            visual_slam_node,
        ],
        output='screen',
    )

    return launch.LaunchDescription([visual_slam_launch_container])
