import cv2
import numpy as np

def draw_masks(img, result, alpha=0.5):
    if result.masks is None:
        return img
    
    masks = result.masks.data.cpu().numpy()
    classes = result.boxes.cls.cpu().numpy()

    overlay = img.copy()

    for mask, cls in zip(masks, classes):
        color = np.random.default_rng(
                int(cls)).integers(0, 255, size=3, dtype=np.uint8
                                   )

        overlay[mask.astype(bool)] = color

    return cv2.addWeighted(
                overlay, 
                alpha, 
                img, 
                1 - alpha,
                0
            )
    
