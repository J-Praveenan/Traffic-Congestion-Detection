# yolo_processor.py

import cv2
import numpy as np
import time
from ultralytics import YOLO
from collections import defaultdict

def get_color_for_id(track_id):
    np.random.seed(track_id)
    return tuple(np.random.randint(0, 255, size=3).tolist())

def draw_text_with_background(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX,
                              font_scale=1, font_thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0), padding=5):
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_width, text_height = text_size

    x, y = position
    top_left = (x, y - text_height - padding)
    bottom_right = (x + text_width + padding * 2, y + padding)

    cv2.rectangle(image, top_left, bottom_right, bg_color, -1)
    cv2.putText(image, text, (x + padding, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

class YOLOVideoProcessor:
    def __init__(self, model_path, video_path, output_path, classes=[0], tracker_method="bot",heavy_threshold=15, moderate_threshold=10):
        self.model = YOLO(model_path, task="detect")
        self.classes = classes
        self.tracker_method = tracker_method
        self.track_colors = {}
        self.track_history = defaultdict(list)
        self.video_path = video_path
        self.output_path = output_path
        self.heavy_threshold = heavy_threshold
        self.moderate_threshold = moderate_threshold

    def is_in_region(self, center, poly):
        poly_np = np.array(poly, dtype=np.int32)
        return cv2.pointPolygonTest(poly_np, center, False) >= 0

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30.0

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # ✅ Define ROI as the full video frame
        roi_polygon = [(0, 0), (frame_width, 0), (frame_width, frame_height), (0, frame_height)]


        fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (frame_width, frame_height))

        tracker_cfg = "botsort.yaml" if self.tracker_method.lower() == "bot" else "bytetrack.yaml"

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model.track(frame, persist=True, tracker=tracker_cfg, classes=self.classes, conf=0.15)

            # ✅ Use xywh (center format) for consistency with tracker
            boxes = results[0].boxes.xywh.cpu().numpy() if results[0].boxes else []
            confidences = results[0].boxes.conf.cpu().numpy() if results[0].boxes else []
            # ✅ Ensure IDs always exist, even if tracker fails
            track_ids = results[0].boxes.id.int().cpu().tolist() if hasattr(results[0].boxes, "id") and results[0].boxes.id is not None else list(range(len(boxes)))

            total_cars = 0
            for box, track_id, conf in zip(boxes, track_ids, confidences):
                total_cars += 1
                x, y, w, h = box
                
                center_point = (int(x), int(y))

                # ✅ Check if inside full-frame ROI (always true, but kept for flexibility)
                if not self.is_in_region(center_point, roi_polygon):
                    continue

                # total_cars += 1
                
                color = get_color_for_id(track_id)

                # Convert from xywh to pixel coordinates
                x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # ID label
                label = f"ID: {track_id}"
                (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (x1, y1 - text_h - 6), (x1 + text_w + 4, y1), color, -1)
                cv2.putText(frame, label, (x1 + 2, y1 - 4),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

                # ✅ Store track history (optional: to draw trajectory)
                center_point = (int(x), int(y))
                self.track_history[track_id].append(center_point)
                if len(self.track_history[track_id]) > 15:
                    self.track_history[track_id].pop(0)

                # Draw motion trail
                pts = np.array(self.track_history[track_id]).reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=False, color=color, thickness=2)

            # ✅ Draw ROI border (yellow)
            cv2.polylines(frame, [np.array(roi_polygon, np.int32)], True, (0, 255, 255), 2)
            
            # Congestion detection
            if total_cars >= self.heavy_threshold:
                congestion = "heavy"
            elif total_cars >= self.moderate_threshold:
                congestion = "moderate"
            else:
                congestion = "smooth"

            draw_text_with_background(frame, f"Total Vehicles: {total_cars}", (7, 50),
                                    bg_color=(0, 0, 0), text_color=(0, 255, 0))
            draw_text_with_background(frame, f"Road Condition: {congestion}", (7, 90),
                                    bg_color=(0, 0, 0), text_color=(0, 255, 0))

            out.write(frame)

        cap.release()
        out.release()



