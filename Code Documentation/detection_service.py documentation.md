# Code Documentation

## Waste Detection Using YOLO Model

This Python script utilizes a pretrained YOLO (You Only Look Once) model to detect and classify objects in images or video frames. The goal is to identify whether detected items are biodegradable or non-biodegradable, useful in waste sorting applications.

---

### Import Statements

```python
import torch
import numpy as np
import time
from ultralytics import YOLO
from categories.biodegradable_items import biodegradable_items
from categories.non_biodegradable_items import non_biodegradable_items
from utils.drawing_utils import draw_detection
```
The script imports necessary libraries and modules. torch enables efficient tensor computations on GPUs/CPUs. numpy assists with array operations. The YOLO class from the Ultralytics package is used to load and run the object detection model. It also imports two predefined lists of biodegradable and non-biodegradable item names, and a utility function draw_detection for visually annotating detected objects on frames.

### Model Initialization
```python
model = YOLO('/home/glide/Documents/PROJECT DEVELOPMENT/etapon-prototype/yolov8n-oiv7.pt')
```
This line loads a custom-trained YOLO model from the specified path. The model is ready to perform inference on input images.

### Counters for Detected Items
```python
biodegradable_counter = 0
non_biodegradable_counter = 0
```
These two variables keep track of the number of detected biodegradable and non-biodegradable objects, respectively.

### Frame Processing Function
```python
def process_frame(frame, biodegradable_counter=0, non_biodegradable_counter=0):
    logs = []
    try:
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

            if confidence >= 0.7:
                if label in biodegradable_items:
                    object_type = "Biodegradable"
                    biodegradable_counter += 1
                elif label in non_biodegradable_items:
                    object_type = "Non-Biodegradable"
                    non_biodegradable_counter += 1
                else:
                    object_type = "Unknown"

                draw_detection(frame, x1, y1, x2, y2, label, object_type, confidence)
                logs.append(f"{object_type} detected: {label} ({confidence:.2f})")
            else:
                continue

        return frame, biodegradable_counter, non_biodegradable_counter, logs
    except Exception as e:
        logs.append(f"Error processing frame: {e}")
        return frame, biodegradable_counter, non_biodegradable_counter, logs
```
The process_frame function is the core component that accepts an image frame as input and processes it to detect objects.
- First, it converts the input frame into a NumPy array suitable for model input.
- It runs inference using the YOLO model in a torch.no_grad() context to disable gradient tracking for efficiency.
- The results contain bounding boxes, confidence scores, and class IDs of detected objects.
- For each detected object, it extracts the bounding box coordinates, confidence level, and class label.
- Only detections with confidence scores of 0.7 or higher are considered valid.
- The detected label is compared against the lists of biodegradable and non-biodegradable items:
    - If the label matches a biodegradable item, it increments the biodegradable_counter.
    - If it matches a non-biodegradable item, it increments the non_biodegradable_counter.
    - Otherwise, it marks the object type as "Unknown."
- It calls draw_detection to visually annotate the frame with bounding boxes and labels.
- Each detection is logged with its classification and confidence score.
- Finally, the function returns the annotated frame, updated counters, and logs.
- If an error occurs during processing, it catches the exception, logs the error message, and returns the frame and counters unchanged.