from ultralytics import YOLO
import cv2
import math


def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)

    model = YOLO("YOLO-Weights/best.pt")
    classNames = ["policja", "policja_na_sygnale", "straz", "straz_na_sygnale", "karetka", "karetka_na_sygnale",
                  "wojsko", "policja_nieoznakowana", "na_sygnale", "brak_sygnalizacji"]

    while True:
        success, img = cap.read()
        results = model(img, imgsz=320, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                conf = math.ceil((box.conf[0]*100))/100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                if class_name == 'policja':
                    color = (0, 204, 255)
                elif class_name == "straz":
                    color = (222, 82, 175)
                elif class_name == "karetka":
                    color = (0, 149, 255)
                else:
                    color = (85, 45, 255)
                if conf > 0.6:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)
                    cv2.putText(img, label, (x1, y1-2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        yield img


cv2.destroyAllWindows()
