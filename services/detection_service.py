import torch
import numpy as np
import time
from ultralytics import YOLO
from categories.biodegradable_items import biodegradable_items
from categories.non_biodegradable_items import non_biodegradable_items
from utils.drawing_utils import draw_detection
from utils.serial_communication_to_arduino import sendSignalToArduino

model = YOLO('my_model.pt')

biodegradable_counter = 0
non_biodegradable_counter = 0

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

            # Process all detections regardless of confidence
            if label in biodegradable_items:
                object_type = "Biodegradable"
                sendSignalToArduino(1)
                biodegradable_counter += 1
            elif label in non_biodegradable_items:
                object_type = "Non-Biodegradable"
                sendSignalToArduino(2)
                non_biodegradable_counter += 1
            else:
                object_type = "Unknown"

            # Draw the detection
            draw_detection(frame, x1, y1, x2, y2, label, object_type, confidence)
            logs.append(f"{object_type} detected: {label} ({confidence:.2f})")

        return frame, biodegradable_counter, non_biodegradable_counter, logs
    except Exception as e:
        logs.append(f"Error processing frame: {e}")
        return frame, biodegradable_counter, non_biodegradable_counter, logs


    
