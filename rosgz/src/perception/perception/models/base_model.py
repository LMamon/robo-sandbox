import torch
from ultralytics import YOLOE

class BaseModel:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLOE('yoloe-26n-seg.pt')
        self.model.to(self.device)
    
    def inference(self, img):
        results = self.model(img, verbose = False)[0]
        
        if results.boxes is not None:
            keep = results.boxes.conf > 0.7 # 70% confidence threshold
            results.boxes = results.boxes[keep]
        
        return results