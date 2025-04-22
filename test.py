import torch
import cv2
import numpy as np
from ultralytics import YOLO
from biodegradable_items import biodegradable_items
from non_biodegradable_items import non_biodegradable_items

# Load the YOLOv8 model
model = YOLO('/models/best.pt')

# Initialize OpenCV video capture (use 0 for the default camera or specify camera index)
cap = cv2.VideoCapture(0)  # 0 typically refers to the default webcam

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

def process_frame(frame):
    # Convert frame to a NumPy array (no resizing needed)
    img_array = np.array(frame)

    # Get predictions from the model
    with torch.no_grad():
        results = model(img_array)

    # Extract predictions
    predictions = results[0].boxes
    class_names = model.names

    # Iterate through detected objects
    for box, conf, cls in zip(predictions.xyxy, predictions.conf, predictions.cls):
        x1, y1, x2, y2 = map(int, box.tolist())  # Convert to integers
        confidence = conf.item()
        class_id = int(cls.item())
        label = class_names[class_id]

        # Determine the object type
        if label in biodegradable_items:
            object_type = "Biodegradable"
            color = (0, 255, 0)  # Green
        elif label in non_biodegradable_items:
            object_type = "Non-Biodegradable"
            color = (0, 0, 255)  # Red
        else:
            object_type = "Unknown"
            color = (255, 0, 0)  # Blue

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f'{label}: {object_type} - {confidence:.2f}', 
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame

# Real-time processing loop
while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Process the frame (object detection + drawing)
    processed_frame = process_frame(frame)

    # Display the result
    cv2.imshow('Real-time Image Processing', processed_frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
