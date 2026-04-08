import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import numpy as np
from scipy.spatial.transform import Rotation as R


def pose_to_vec(pose):
    return np.array([pose.position.x, pose.position.y, pose.position.z])


def pose_to_matrix(pose):
    t = pose_to_vec(pose)
    q = [pose.orientation.x, pose.orientation.y,
         pose.orientation.z, pose.orientation.w]
    rot = R.from_quat(q).as_matrix()

    T = np.eye(4)
    T[:3, :3] = rot
    T[:3, 3] = t
    return T


def matrix_to_pose(T):
    pose = PoseStamped()
    pose.pose.position.x = T[0, 3]
    pose.pose.position.y = T[1, 3]
    pose.pose.position.z = T[2, 3]

    quat = R.from_matrix(T[:3, :3]).as_quat()
    pose.pose.orientation.x = quat[0]
    pose.pose.orientation.y = quat[1]
    pose.pose.orientation.z = quat[2]
    pose.pose.orientation.w = quat[3]

    return pose


def umeyama_sim3(src, dst):
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)

    src_c = src - src_mean
    dst_c = dst - dst_mean

    H = src_c.T @ dst_c / src.shape[0]

    U, S, Vt = np.linalg.svd(H)
    R_est = Vt.T @ U.T

    if np.linalg.det(R_est) < 0:
        Vt[-1, :] *= -1
        R_est = Vt.T @ U.T

    var_src = np.sum(src_c**2) / src.shape[0]
    scale = np.sum(S) / var_src

    t_est = dst_mean - scale * R_est @ src_mean

    return scale, R_est, t_est


class AlignedPathPublisher(Node):
    def __init__(self):
        super().__init__('aligned_path_publisher')

        self.gt_buffer = []   #[(t, vec)]
        self.vio_buffer = []  #[(t, vec)]

        self.T_align = None

        self.window_size = 100
        self.max_dt = 0.05  # 20ms tolerance

        self.gt_sub = self.create_subscription(
            PoseStamped, '/gt_pose', self.gt_callback, 10)

        self.vio_sub = self.create_subscription(
            Path, '/ov_msckf/pathimu', self.vio_callback, 10)

        self.pub = self.create_publisher(
            Path, '/ov_msckf/pathimu_aligned', 10)

        self.path = Path()
        self.path.header.frame_id = "global"

    def stamp_to_sec(self, stamp):
        return stamp.sec + stamp.nanosec * 1e-9

    def gt_callback(self, msg):
        t = self.stamp_to_sec(msg.header.stamp)
        self.gt_buffer.append((t, pose_to_vec(msg.pose)))

    def vio_callback(self, msg):
        if not msg.poses:
            return

        latest = msg.poses[-1]
        t = self.stamp_to_sec(latest.header.stamp)

        self.vio_buffer.append((t, pose_to_vec(latest.pose)))

        src, dst = self.get_aligned_pairs()

        if len(src) < 15:
            return

        # sliding window
        src = src[-self.window_size:]
        dst = dst[-self.window_size:]

        scale, R_est, t_est = umeyama_sim3(src, dst)

        self.T_align = np.eye(4)
        self.T_align[:3, :3] = scale * R_est
        self.T_align[:3, 3] = t_est

        #transform
        T_vio = pose_to_matrix(latest.pose)
        T_aligned = self.T_align @ T_vio

        aligned_pose = matrix_to_pose(T_aligned)

        aligned_pose.header.stamp = latest.header.stamp
        aligned_pose.header.frame_id = "global"

        self.path.header.stamp = latest.header.stamp
        self.path.poses.append(aligned_pose)

        self.pub.publish(self.path)

    def get_aligned_pairs(self):
        gt = []
        vio = []

        if not self.gt_buffer or not self.vio_buffer:
            return np.array([]), np.array([])

        gt_idx = 0

        for t_vio, p_vio in self.vio_buffer:
            while (gt_idx + 1 < len(self.gt_buffer) and
                   abs(self.gt_buffer[gt_idx + 1][0] - t_vio) <
                   abs(self.gt_buffer[gt_idx][0] - t_vio)):
                gt_idx += 1

            t_gt, p_gt = self.gt_buffer[gt_idx]

            if abs(t_gt - t_vio) < self.max_dt:
                vio.append(p_vio)
                gt.append(p_gt)

        return np.array(vio), np.array(gt)


def main():
    rclpy.init()
    node = AlignedPathPublisher()
    rclpy.spin(node)
    rclpy.shutdown()