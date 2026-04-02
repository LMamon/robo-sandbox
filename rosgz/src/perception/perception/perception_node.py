import rclpy
import torch
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from perception.models.base_model import BaseModel
from perception.tasks.detections import draw_bbox
from perception.tasks.segmentation import draw_masks


class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.bridge = CvBridge()
        self.model = BaseModel()

        self.rgb_sub = self.create_subscription(
            Image, 
            '/px4vision/rgb/image', 
            self.image_callback, 
            10 
        )
        self.seg_publisher = self.create_publisher(
            Image,
            '/perception/instance_seg/image',
            10,
        )
        self.det_publisher = self.create_publisher(
            Image,
            '/perception/detections/image',
            10,
        )

    def image_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        #image size is (480, 640, 3)
        
        results = self.model.inference(img)

        det_img = draw_bbox(img.copy(), results)
        seg_img = draw_masks(img.copy(), results)
    
        det_img = self.bridge.cv2_to_imgmsg(det_img, encoding='bgr8')
        seg_img = self.bridge.cv2_to_imgmsg(seg_img, encoding='bgr8')

        self.det_publisher.publish(det_img)
        self.seg_publisher.publish(seg_img)


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node) #event loop
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()