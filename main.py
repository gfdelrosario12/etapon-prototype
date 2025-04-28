from camera.webcam import get_camera, read_frame
from services.detection_service import process_frame
import cv2

picam2 = get_camera()

try:
    while True:
        frame = read_frame(picam2)

        processed_frame = process_frame(frame)
        cv2.imshow('Real-time Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    cv2.destroyAllWindows()