# Import required libraries
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
from categories.biodegradable_items import biodegradable_items
from categories.non_biodegradable_items import non_biodegradable_items

# Load the YOLOv8 model (.pt file)
model = YOLO('best.pt')

# Initialize and configure the PiCamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

def process_frame(frame):
    """
    Process a single frame: detect objects, classify them, and draw bounding boxes.
    """
    img_array = np.array(frame)

    # Run object detection
    with torch.no_grad():
        results = model(img_array)

    # Extract predictions
    predictions = results[0].boxes
    class_names = model.names

    # Iterate through detected objects
    for box, conf, cls in zip(predictions.xyxy, predictions.conf, predictions.cls):
        x1, y1, x2, y2 = map(int, box.tolist())
        confidence = conf.item()
        class_id = int(cls.item())
        label = class_names[class_id]

        # Determine object type and color
        if label in biodegradable_items:
            object_type = "Biodegradable"
            color = (0, 255, 0)  # Green
        elif label in non_biodegradable_items:
            object_type = "Non-Biodegradable"
            color = (0, 0, 255)  # Red
        else:
            object_type = "Unknown"
            color = (255, 0, 0)  # Blue

        # Draw bounding box and label on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {object_type} ({confidence:.2f})',
                    (x1, max(y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame

# Main real-time loop
try:
    while True:
        # Capture frame from PiCamera2
        frame = picam2.capture_array()

        # Process frame
        processed_frame = process_frame(frame)

        # Display frame
        cv2.imshow('Real-time Waste Classification', processed_frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup resources
    cv2.destroyAllWindows()
    picam2.stop()
