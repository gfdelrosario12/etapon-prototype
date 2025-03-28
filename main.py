import torch
import cv2
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items

cv2.setUseOptimized(True)

# Load the YOLOv8 model
model = YOLO('fine-tuned/yolov8n-oiv7.pt')

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

INPUT_SIZE = 320  # YOLOv8 expects square inputs

def process_frame(frame):
    """Processes the frame and draws bounding boxes."""
    h, w, _ = frame.shape

    # Perform inference
    with torch.no_grad():
        results = model(frame)

    predictions = results[0].boxes
    class_names = model.names  # Dictionary of class names

    for pred in predictions:
        x1, y1, x2, y2 = map(int, pred.xyxy[0].tolist())  # Get absolute coordinates
        confidence = pred.conf[0].item()
        class_id = int(pred.cls[0].item())
        label = class_names.get(class_id, "Unknown")  # Get class name safely

        if confidence < 0.4:  # Confidence threshold
            continue

        # Determine object type and color
        if label in biodegradable_items:
            object_type, color = "Biodegradable", (0, 255, 0)
        elif label in non_biodegradable_items:
            object_type, color = "Non-Biodegradable", (0, 0, 255)
        else:
            object_type, color = "Unknown", (255, 0, 0)

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {object_type} - {confidence:.2f}', 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame

frame_skip = 2  # Process every 2nd frame for better FPS
frame_count = 0

while True:
    frame = picam2.capture_array()  # Capture frame as NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Process every N frames for performance
    if frame_count % frame_skip == 0:
        processed_frame = process_frame(frame)
        cv2.imshow('Object Detection', processed_frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()