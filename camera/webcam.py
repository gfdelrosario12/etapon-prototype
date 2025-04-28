from picamera2 import Picamera2
import cv2
import numpy as np

def get_camera():
<<<<<<< Updated upstream
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
        picam2.start()
        return picam2
    except Exception as e:
        print(f"Error initializing camera: {e}")
        print("Check get_camera() function in webcam.py")
        return None
    
def read_frame(picam2):
    try:
        # Get RGB frame as a NumPy array
        frame = picam2.capture_array()
        return frame
    except Exception as e:
        print(f"Error capturing frame: {e}")
        print("Check read_frame() function in webcam.py")
        return None
=======
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    picam2.start()
    return picam2

def read_frame(picam2):
    # Get RGB frame as a NumPy array
    frame = picam2.capture_array()
    return frame
>>>>>>> Stashed changes
