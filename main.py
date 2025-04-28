from camera.webcam import get_camera, read_frame
from services.detection_service import process_frame
from controllers.servo_controller import cleanup
import cv2

picam2 = get_camera()

try:
    while True:
        try:
            frame = read_frame(picam2)

            processed_frame = process_frame(frame)
            cv2.imshow('Real-time Detection', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error processing frame: {e}")
            print("Check main.py")
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    try:
        cv2.destroyAllWindows()
        cleanup()
    except Exception as e:
        print(f"Error during cleanup: {e}")
        print("Check main.py cleanup section")