import torch
import cv2
import numpy as np
from ultralytics import YOLO
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items
from servo_controller import move_biodegradable_servo, move_nonbiodegradable_servo, cleanup

# Load YOLOv8 model
model = YOLO('/models/best.pt')

# Start camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def process_frame(frame):
    img_array = np.array(frame)
    with torch.no_grad():
        results = model(img_array)

    predictions = results[0].boxes
    class_names = model.names

    for box, conf, cls in zip(predictions.xyxy, predictions.conf, predictions.cls):
        x1, y1, x2, y2 = map(int, box.tolist())
        confidence = conf.item()
        class_id = int(cls.item())
        label = class_names[class_id]

        if label in biodegradable_items:
            object_type = "Biodegradable"
            color = (0, 255, 0)
            move_biodegradable_servo()
        elif label in non_biodegradable_items:
            object_type = "Non-Biodegradable"
            color = (0, 0, 255)
            move_nonbiodegradable_servo()
        else:
            object_type = "Unknown"
            color = (255, 0, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {object_type} - {confidence:.2f}',
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        processed_frame = process_frame(frame)
        cv2.imshow('Real-time Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    cleanup()
