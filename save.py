<<<<<<< Updated upstream
# Import required libraries
=======
>>>>>>> Stashed changes
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from picamera2 import Picamera2
<<<<<<< Updated upstream
from categories.biodegradable_items import biodegradable_items
from categories.non_biodegradable_items import non_biodegradable_items

# Load the YOLOv8 model (.pt file)
model = YOLO('best.pt')

# Initialize and configure the PiCamera2
=======
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items

# Load the YOLOv8 model
model = YOLO('yolov8n-oiv7.pt')

# Initialize Picamera2
>>>>>>> Stashed changes
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

def process_frame(frame):
<<<<<<< Updated upstream
    """
    Process a single frame: detect objects, classify them, and draw bounding boxes.
    """
    img_array = np.array(frame)

    # Run object detection
=======
    # Convert frame to a NumPy array (no resizing needed)
    img_array = np.array(frame)

    # Get predictions from the model
>>>>>>> Stashed changes
    with torch.no_grad():
        results = model(img_array)

    # Extract predictions
    predictions = results[0].boxes
    class_names = model.names

    # Iterate through detected objects
    for box, conf, cls in zip(predictions.xyxy, predictions.conf, predictions.cls):
<<<<<<< Updated upstream
        x1, y1, x2, y2 = map(int, box.tolist())
=======
        x1, y1, x2, y2 = map(int, box.tolist())  # Convert to integers
>>>>>>> Stashed changes
        confidence = conf.item()
        class_id = int(cls.item())
        label = class_names[class_id]

<<<<<<< Updated upstream
        # Determine object type and color
=======
        # Determine the object type
>>>>>>> Stashed changes
        if label in biodegradable_items:
            object_type = "Biodegradable"
            color = (0, 255, 0)  # Green
        elif label in non_biodegradable_items:
            object_type = "Non-Biodegradable"
            color = (0, 0, 255)  # Red
        else:
            object_type = "Unknown"
            color = (255, 0, 0)  # Blue

<<<<<<< Updated upstream
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
=======
        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {object_type} - {confidence:.2f}', 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return frame

# Real-time processing loop
while True:
    # Capture frame from Picamera2
    frame = picam2.capture_array()

    # Process the frame (object detection + drawing)
    processed_frame = process_frame(frame)

    # Display the result
    cv2.imshow('Real-time Image Processing', processed_frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()
>>>>>>> Stashed changes
