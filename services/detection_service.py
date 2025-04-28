import torch
import numpy as np
<<<<<<< Updated upstream
import time
=======
>>>>>>> Stashed changes
from ultralytics import YOLO
from categories.biodegradable_items import biodegradable_items
from categories.non_biodegradable_items import non_biodegradable_items
from utils.drawing_utils import draw_detection
from utils.serial_communication_to_arduino import sendSignalToArduino

model = YOLO('models/best.pt')

def process_frame(frame):
<<<<<<< Updated upstream
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

            if label in biodegradable_items:
                object_type = "Biodegradable"
                sendSignalToArduino(1)
            elif label in non_biodegradable_items:
                object_type = "Non-Biodegradable"
                sendSignalToArduino(2)
            else:
                object_type = "Unknown"

            draw_detection(frame, x1, y1, x2, y2, label, object_type, confidence)
            time.sleep(10)
        return frame
    except Exception as e:
        print(f"Error processing frame: {e}")
        print("Check process_frame() function in detection_service.py")
        return None
    
=======
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
            sendSignalToArduino(1)
            time.sleep(10000)
        elif label in non_biodegradable_items:
            object_type = "Non-Biodegradable"
            sendSignalToArduino(2)
            time.sleep(10000)
        else:
            object_type = "Unknown"

        draw_detection(frame, x1, y1, x2, y2, label, object_type, confidence)

    return frame
>>>>>>> Stashed changes
