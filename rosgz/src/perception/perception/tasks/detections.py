import cv2

def draw_bbox(img, result):
    if result.boxes is None:
        return img

    names = result.names

    for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf)
            cls = int(box.cls)

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
                org=(x1, max(0, y1 - 5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255,0, 0),
                thickness=1,
                lineType=cv2.LINE_AA
            )
    return img
