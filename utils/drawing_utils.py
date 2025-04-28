import cv2

def draw_detection(frame, x1, y1, x2, y2, label, object_type, confidence):
    color_map = {
        "Biodegradable": (0, 255, 0),
        "Non-Biodegradable": (0, 0, 255),
        "Unknown": (255, 0, 0)
    }
    color = color_map.get(object_type, (255, 255, 255))

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, f'{label}: {object_type} - {confidence:.2f}',
                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)