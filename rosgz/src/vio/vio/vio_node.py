import rclpy
import numpy as np
from scipy.spatial.transform import Rotation as R
from rclpy.node import Node
from nav_msgs.msg import Odometry
from px4_msgs.msg import VehicleOdometry


class VIONode(Node):
    def __init__(self):
        super().__init__('vio_node')

        self.ov_imu_sub = self.create_subscription(
            Odometry,
            '/visual_slam/tracking/odometry',
            self.odom_callback,
            10
        )

        self.vvo_pub = self.create_publisher(
            VehicleOdometry,
            '/fmu/in/vehicle_visual_odometry',
            10
        )

    #TODO: add imu_callback
    def odom_callback(self, msg):
        vvo = VehicleOdometry()
        
        # fill from msg.pose + msg.twist
        # convert ENU > NED
        pos = msg.pose.pose.position
        vel = msg.twist.twist.linear
        q = msg.pose.pose.orientation
        ang = msg.twist.twist.angular
        now = int(msg.header.stamp.sec * 1_000_000 + msg.header.stamp.nanosec // 1000)

        if not hasattr(self, "origin"):
            self.origin = pos

        x_local = pos.x - self.origin.x
        y_local = pos.y - self.origin.y
        z_local = pos.z - self.origin.z

        x_ned = y_local
        y_ned = x_local
        z_ned = -z_local

        q_enu = [q.x, q.y, q.z, q.w]
        
        #convert quaternion from ENU to NED
        r_enu = R.from_quat(q_enu)
        R_enu_to_ned = R.from_matrix([
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1]
        ])
        r_ned = R_enu_to_ned * r_enu * R_enu_to_ned.inv()
        
        q_ned = r_ned.as_quat()
        q_ned = q_ned / np.linalg.norm(q_ned)

        vvo.timestamp = now
        vvo.timestamp_sample = now

        vvo.pose_frame = VehicleOdometry.POSE_FRAME_NED
        vvo.velocity_frame = VehicleOdometry.VELOCITY_FRAME_NED

        vvo.position = np.array([x_ned, y_ned, z_ned], dtype=np.float32)

        vvo.velocity = np.array([float('nan'), float('nan'), float('nan')], dtype=np.float32)
        vvo.q = np.array([
            q_ned[3],
            q_ned[0],
            q_ned[1],
            q_ned[2]
        ], dtype=np.float32)

        vvo.angular_velocity = np.array([float('nan'), float('nan'), float('nan')], dtype=np.float32)

        vvo.velocity_variance = np.array([999.0, 999.0, 999.0], dtype=np.float32)

        vvo.position_variance = np.array([0.05, 0.05, 0.1], dtype=np.float32)
        vvo.orientation_variance = np.array([999.0, 999.0, 999.0], dtype=np.float32)
        vvo.quality = 1

        self.vvo_pub.publish(vvo)


def main(args=None):
    rclpy.init(args=args)
    node = VIONode()
    rclpy.spin(node) #event loop
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()