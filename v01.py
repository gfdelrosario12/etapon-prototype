import torch
import cv2
import numpy as np
from ultralytics import YOLO
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items

cv2.setUseOptimized(True)

# Load YOLOv8 model (ONNX format)
model = YOLO('fine-tuned/yolov8n-oiv7.onnx')

# Webcam settings
ORIG_WIDTH, ORIG_HEIGHT = 640, 480
INPUT_SIZE = 320  # YOLOv8 input size

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, ORIG_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ORIG_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 15)  # Adjust FPS for performance

def process_frame(frame):
    """Processes the frame and draws bounding boxes efficiently."""
    h, w, _ = frame.shape

    # Resize frame to YOLO input size
    img_resized = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))

    with torch.no_grad():
        results = model(img_resized)

    predictions = results[0].boxes
    class_names = model.names

    scale_x, scale_y = w / INPUT_SIZE, h / INPUT_SIZE

    for pred in predictions:
        x1, y1, x2, y2 = pred.xyxy[0].tolist()
        confidence = pred.conf[0].item()
        class_id = int(pred.cls[0].item())
        label = class_names[class_id]

        # Scale coordinates back to original size
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)

        # Determine category and color
        if label in biodegradable_items:
            color, category = (0, 255, 0), "Biodegradable"
        elif label in non_biodegradable_items:
            color, category = (0, 0, 255), "Non-Biodegradable"
        else:
            color, category = (255, 0, 0), "Unknown"

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {category} ({confidence:.2f})',
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame

frame_skip, frame_count = 2, 0  # Skip every 2nd frame for better FPS

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_skip == 0:
        processed_frame = process_frame(frame)
        cv2.imshow('Object Detection', processed_frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()