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
            '/ov_msckf/odomimu',
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
        now = msg.header.stamp.sec * 1_000_000 + msg.header.stamp.nanosec // 1000.  #self.get_clock().now().nanoseconds // 1000

        x_ned = pos.y
        y_ned = pos.x
        z_ned = -pos.z

        vx = vel.y
        vy = vel.x
        vz = -vel.z

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

        wx = ang.y
        wy = ang.x
        wz = -ang.z

        vvo.timestamp = now
        vvo.timestamp_sample = now

        vvo.pose_frame = VehicleOdometry.POSE_FRAME_NED
        vvo.velocity_frame = VehicleOdometry.VELOCITY_FRAME_NED

        vvo.position = np.array([x_ned, y_ned, z_ned], dtype=np.float32)
        vvo.velocity = np.array([vx, vy, vz], dtype=np.float32)
        vvo.q = np.array(q_ned, dtype=np.float32)
        vvo.angular_velocity = np.array([wx, wy, wz], dtype=np.float32)
        vvo.velocity_variance = np.array([0.01, 0.01, 0.01], dtype=np.float32)

        vvo.position_variance = np.array([0.01, 0.01, 0.01], dtype=np.float32)
        vvo.orientation_variance = np.array([0.01, 0.01, 0.01], dtype=np.float32)
        vvo.quality = 1

        
        self.vvo_pub.publish(vvo)
        return


def main(args=None):
    rclpy.init(args=args)
    node = VIONode()
    rclpy.spin(node) #event loop
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()