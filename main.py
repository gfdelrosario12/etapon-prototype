from picamera2 import Picamera2
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items

cv2.setUseOptimized(True)

# Load the YOLOv8 model
model = YOLO('fine-tuned/yolov8n-oiv7.pt')

# Set camera resolution
ORIG_WIDTH, ORIG_HEIGHT = 640, 480
INPUT_SIZE = 320  # YOLOv8 expects square inputs

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (ORIG_WIDTH, ORIG_HEIGHT), "format": "RGB888"})
picam2.configure(config)
picam2.start()

def process_frame(frame):
    """Processes the frame and draws bounding boxes with correct scaling."""
    h, w, _ = frame.shape
    
    # Resize frame to YOLO input size
    img_resized = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))
    img_array = np.array(img_resized, dtype=np.uint8)

    # Perform inference
    with torch.no_grad():
        results = model(img_array)

    predictions = results[0].boxes
    class_names = model.names

    scale_x = w / INPUT_SIZE  # Scale factor for x-coordinates
    scale_y = h / INPUT_SIZE  # Scale factor for y-coordinates

    for pred in predictions:
        x1, y1, x2, y2 = pred.xyxy[0].tolist()  # Get raw coordinates
        confidence = pred.conf[0].item()
        class_id = int(pred.cls[0].item())
        label = class_names[class_id]

        # Rescale coordinates to original frame size
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)

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

frame_skip = 1  # Skip alternate frames to improve FPS
frame_count = 0

while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR for OpenCV

    # Process every frame (or every alternate frame if needed)
    if frame_count % frame_skip == 0:
        processed_frame = process_frame(frame)
        cv2.imshow('Object Detection', processed_frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()