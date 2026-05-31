import os
import yaml
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource 
from launch.actions import ExecuteProcess, TimerAction, IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import LogInfo

def generate_launch_description():
    bridge_yaml = os.path.join(get_package_share_directory('rxsim'), 'config/bridge.yaml')
    topics_yaml = os.path.join(get_package_share_directory('rxsim'), 'config/topics.yaml')

    with open(topics_yaml) as f:
        topics = yaml.safe_load(f)['topics']
        cmd = ['ros2', 'bag', 'record'] + topics + ['-s', 'mcap']

    
    uxrce_agent = ExecuteProcess(
        cmd=['MicroXRCEAgent', 'udp4', '-p', '8888'],
        output='screen'
    )
    ros_bag = ExecuteProcess(cmd=cmd, output='screen')

    bridge_node = Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    name='gz_parameter_bridge',
                    parameters=[{'config_file': bridge_yaml}],
                    output='screen'
                )
    stereo_node = Node(
                    package='vio',
                    executable='stereo_sync',
                    name='stereo_sync',
                    parameters=[{"use_sim_time": True}],
                    output='screen'
    )

    square_mode_node = Node(
                    package='rxsim_offboard',
                    executable='square_mode_node',
                    name='square_mode_node',
                    output='screen'
                )

    vslam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rxsim'),
                'launch',
                'cu_vslam.launch.py'
            )
        ),
    )

    nvblox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('rxsim'),
                'launch',
                'nvblox.launch.py'
            )
        )
    )

    static_tf_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0", "0", "0",
            "0", "0", "0",
            "base_link",
            "px4vision/base_link/imu_sensor"
        ],
    )
    
    static_tf_left_camera_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0", "0", "0",
            "-0.5", "0.5", "-0.5", "0.5",
            "px4vision/left_camera_link",
            "left_camera_optical"
        ],
    )

    static_tf_right_camera_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0", "0", "0",
            "-0.5", "0.5", "-0.5", "0.5",
            "px4vision/right_camera_link",
            "right_camera_optical"
        ],
    )

    # static_tf_world = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments=[
    #         "0", "0", "0",
    #         "0", "0", "0",
    #         "global",
    #         "rxsim1"
    #     ],
    # )

    # static_tf_map_rxsim = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments=[
    #         "0", "0", "0",
    #         "0", "0", "0",
    #         "rxsim1",
    #         "map"
    #     ],
    # )

    # static_tf_map_odom = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     arguments=[
    #         "0", "0", "0",
    #         "0", "0", "0",
    #         "map",
    #         "odom"
    #     ],
    # )

    static_tf_base_link_left = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0.19", "0.05", "-0.012",
            "0", "0", "0",
            "base_link",
            "px4vision/left_camera_link"
        ],
    )

    static_tf_base_link_right = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0.19", "-0.05", "-0.012",
            "0", "0", "0",
            "base_link",
            "px4vision/right_camera_link"
        ],
    )
    static_tf_base_link_depth = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0.09", "-0.032", "-0.012",
            "0", "0", "0",
            "base_link",
            "px4vision/depth_camera_link"
        ],
    )

    static_tf_depth_camera_optical = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0", "0", "0",
            "-0.5", "0.5", "-0.5", "0.5",
            "px4vision/depth_camera_link",
            "depth_camera_optical"
        ],
    )

    static_tf_depth_camera_link = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            "0", "0", "0",
            "-0.5", "0.5", "-0.5", "0.5",
            "px4vision/depth_camera_link",
            "px4vision/depth_camera_link/depth_camera"
        ],
    )
    vio_node = Node(
                    package='vio',
                    executable='vio_node',
                    name='vio_node',
                    parameters=[{"use_sim_time": True}],
                    output='screen'
                )
    # gt_path_node = Node(
    #                 package='vio',
    #                 executable='gt_path_publisher',
    #                 name='gt_path_publisher',
    #                 parameters=[{"use_sim_time": True}],
    #                 output='screen'
    #             )

    # foxglove_bridge = Node(
    #         package='foxglove_bridge',
    #         executable='foxglove_bridge',
    #         name='foxglove_bridge',
    #         output='screen',
    #         parameters=[{
    #             'topic_whitelist': topics,
    #             'send_buffer_limit': 10000000,
    #             'max_qos_depth': 1,
    #         }]
    #     )
        # TODO: fine tune models and use for live SDT
    # perception_node = Node(
    #         package='perception',
    #         executable='perception_node',
    #         name='perception_node',
    #         output='screen'
    #     )
       
    return LaunchDescription([
        bridge_node,
        static_tf_imu,
        static_tf_base_link_left,
        static_tf_base_link_right,
        static_tf_left_camera_link,
        static_tf_right_camera_link,
        static_tf_base_link_depth,
        static_tf_depth_camera_optical,
        static_tf_depth_camera_link,
        TimerAction(period=0.5, actions=[uxrce_agent]),
        TimerAction(period=1.0, actions=[stereo_node]),
        TimerAction(period=2.0, actions=[vio_node]),
        TimerAction(period=3.0, actions=[vslam_launch]),
        TimerAction(period=5.0, actions=[nvblox_launch]),
        TimerAction(period=10.0, actions=[ros_bag]),
        TimerAction(period=19.0, actions=[square_mode_node]),
        TimerAction(
            period=20.0,
            actions=[LogInfo(msg="SYSTEM READY - start PX4 now")]
        )
    ])
