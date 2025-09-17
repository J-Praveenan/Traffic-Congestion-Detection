# your_yolo_module.py
def run_detection(image):
    # Use your YOLO model to detect vehicles
    # Here you return the image with bounding boxes and a metadata dict
    annotated_img = image  # Replace this with real annotated frame
    details = {
        "fps": 23,
        "total_cars": 7,
        "left_street_cars": 0,
        "right_street_cars": 0,
        "road_condition": "smooth"
    }
    return annotated_img, details
