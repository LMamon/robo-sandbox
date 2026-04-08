import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

class GtPathPublisher(Node):
    def __init__(self):
        super().__init__('gt_path_publisher')

        self.sub = self.create_subscription(
            PoseStamped,
            '/gt_pose',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            Path,
            '/gt_path',
            10
        )

        self.path = Path()
        self.path.header.frame_id = "rxsim1"

    def callback(self, msg):
        self.path.header.stamp = msg.header.stamp
        self.path.header.frame_id = msg.header.frame_id
        
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.pose

        self.path.poses.append(pose)

        self.pub.publish(self.path)


def main():
    rclpy.init()
    node = GtPathPublisher()
    rclpy.spin(node)
    rclpy.shutdown()