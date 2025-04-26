from picamera2 import Picamera2
import cv2
import numpy as np

def get_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    picam2.start()
    return picam2

def read_frame(picam2):
    # Get RGB frame as a NumPy array
    frame = picam2.capture_array()
    return frame
