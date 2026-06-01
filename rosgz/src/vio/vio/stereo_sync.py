import copy
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image, CameraInfo
from message_filters import Subscriber, ApproximateTimeSynchronizer


class StereoSyncNode(Node):
    def __init__(self):
        super().__init__('stereo_sync_node')

        left_topic = '/px4vision/rgb/left/image'
        right_topic = '/px4vision/rgb/right/image'
        left_info_topic = '/px4vision/rgb/left/camera_info'
        right_info_topic = '/px4vision/rgb/right/camera_info'

        # message_filters subscribers (NOT normal ROS subs)
        self.left_sub = Subscriber(self, Image, left_topic)
        self.left_info_sub = Subscriber(self, CameraInfo, left_info_topic)
        self.right_sub = Subscriber(self, Image, right_topic)
        self.right_info_sub = Subscriber(self, CameraInfo, right_info_topic)

        # Approx sync
        self.sync = ApproximateTimeSynchronizer(
            [self.left_sub, self.right_sub, self.left_info_sub, self.right_info_sub],
            queue_size=20,
            slop=0.05
        )
        self.sync.registerCallback(self.stereo_callback)

        self.left_pub = self.create_publisher(Image, '/stereo/left', 10)
        self.left_info_pub = self.create_publisher(CameraInfo, '/stereo/left/camera_info', 10)
        self.right_pub = self.create_publisher(Image, '/stereo/right', 10)
        self.right_info_pub = self.create_publisher(CameraInfo, '/stereo/right/camera_info', 10)

        self.get_logger().info("Stereo sync node initialized")

    def stereo_callback(self, left_img: Image, right_img: Image, left_info: CameraInfo, right_info: CameraInfo):
        # fire ONLY when both frames are time-aligned
        left_info_sync = copy.copy(left_info)
        left_info_sync.header.stamp = left_img.header.stamp

        left_img_sync = copy.copy(left_img)
        left_img_sync.header.stamp = left_img.header.stamp

        right_info_sync = copy.copy(right_info)
        right_info_sync.header.stamp = left_img.header.stamp

        right_img_sync = copy.copy(right_img)
        right_img_sync.header.stamp = left_img.header.stamp
        
        baseline = 0.10
        fx = left_info.k[0]

        left_info_sync.p[3] = 0.0
        right_info_sync.p[3] = -fx * baseline

        left_img_sync.header.frame_id = "left_camera_optical"
        right_img_sync.header.frame_id = "right_camera_optical"

        left_info_sync.header.frame_id = "left_camera_optical"
        right_info_sync.header.frame_id = "right_camera_optical"

        self.left_pub.publish(left_img_sync)
        self.right_pub.publish(right_img_sync)

        self.left_info_pub.publish(left_info_sync)
        self.right_info_pub.publish(right_info_sync)


def main(args=None):
    rclpy.init(args=args)
    node = StereoSyncNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()