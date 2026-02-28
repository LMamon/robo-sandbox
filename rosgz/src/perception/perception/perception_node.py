import rclpy
import cv2
import torch
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLOE

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.bridge = CvBridge()
        self.model = YOLOE('yoloe-26s-seg.pt')
        self.model.to(self.device)
        
        self.rgb_sub = self.create_subscription(
            Image, 
            '/px4vision/rgb/image', 
            self.image_callback, 
            10 
        )
        self.publisher = self.create_publisher(
            Image,
            '/perception/instance_seg/image',
            10,
        )

        self.rgb_sub

    def image_callback(self, msg):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        #image size is (480, 640, 3)
        results = self.model(img, verbose=False)

        result = results[0]
            
        if result.boxes is None or len(result.boxes) == 0: 
            ros_img = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
            self.publisher.publish(ros_img)
            return 
        
        boxes = result.boxes.xyxy.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        for box, conf, cls in zip(boxes, confs, classes):
            x1, y1, x2, y2 = box.astype(int)
            label = f"{result.names[int(cls)]} {conf:.2f}"
            cv2.rectangle(
                    img=img,
                    pt1=(x1, y1),
                    pt2=(x2, y2),
                    color=(255, 0, 0),
                    thickness=2
            )
            cv2.putText(
                img=img,
                text=label,
                org=(x1, y1 - 5),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255,0, 0),
                thickness=1,
                lineType=cv2.LINE_AA
            )
        
        ros_img = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
        self.publisher.publish(ros_img)


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node) #event loop
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()