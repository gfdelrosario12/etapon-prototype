from picamera2 import Picamera2
import numpy as np

def get_camera():
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
        picam2.start()
        return picam2
    except Exception as e:
        print(f"Error initializing Pi Camera: {e}")
        print("Check get_camera() function in webcam.py")
        return None

def read_frame(picam2):
    try:
        frame = picam2.capture_array()
        return frame
    except Exception as e:
        print(f"Error capturing frame: {e}")
        print("Check read_frame() function in webcam.py")
        return None
