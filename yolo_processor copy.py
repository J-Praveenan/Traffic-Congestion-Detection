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
    def __init__(self, model_path, video_path, output_path, classes=[0], tracker_method="bot"):
        self.model = YOLO(model_path, task="detect")
        self.classes = classes
        self.tracker_method = tracker_method
        self.track_colors = {}
        self.track_history = defaultdict(list)
        self.video_path = video_path
        self.output_path = output_path

    def is_in_region(self, center, poly):
        poly_np = np.array(poly, dtype=np.int32)
        return cv2.pointPolygonTest(poly_np, center, False) >= 0

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        prev_frame_time = 0

        poly1 = [(465, 350), (609, 350), (520, 630), (3, 630)]
        poly2 = [(678, 350), (815, 350), (1203, 630), (743, 630)]

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fourcc = cv2.VideoWriter_fourcc(*'H', '2', '6', '4')
        out = cv2.VideoWriter(self.output_path, fourcc, 30, (frame_width, frame_height))

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            tracker = "botsort.yaml" if self.tracker_method.lower() == "bot" else "bytetrack.yaml"
            results = self.model.track(frame, persist=True, tracker=tracker, classes=self.classes, conf=0.25)

            boxes = results[0].boxes.xywh.cpu().numpy() if results[0].boxes else []
            confidences = results[0].boxes.conf.cpu().numpy() if results[0].boxes else []
            track_ids = results[0].boxes.id.int().cpu().tolist() if hasattr(results[0].boxes, "id") else list(range(len(boxes)))

            annotated_frame = frame.copy()
            cv2.polylines(annotated_frame, [np.array(poly1, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)
            cv2.polylines(annotated_frame, [np.array(poly2, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

            current_region1_ids = set()
            current_region2_ids = set()

            for box, track_id, confidence in zip(boxes, track_ids, confidences):
                x, y, w, h = box
                color = get_color_for_id(track_id)

                cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)),
                              (int(x + w / 2), int(y + h / 2)), color, 2)
                draw_text_with_background(annotated_frame, f'ID: {track_id} ({confidence:.2f})',
                                          (int(x - w / 2), int(y - h / 2) - 10), bg_color=color)

                center_point = (int(x), int(y))
                cv2.circle(annotated_frame, center_point, radius=4, color=color, thickness=-1)
                center = (float(x), float(y))
                self.track_history[track_id].append(center)

                if len(self.track_history[track_id]) > 15:
                    self.track_history[track_id].pop(0)

                points = np.array(self.track_history[track_id]).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=color, thickness=2)

                if self.is_in_region(center_point, poly1):
                    current_region1_ids.add(track_id)
                if self.is_in_region(center_point, poly2):
                    current_region2_ids.add(track_id)

            fps = int(1 / (time.time() - prev_frame_time + 1e-8))
            prev_frame_time = time.time()

            draw_text_with_background(annotated_frame, f'FPS: {fps}', (7, 30), bg_color=(0, 0, 0), text_color=(0, 255, 0))
            draw_text_with_background(annotated_frame, f'Total Cars: {len(track_ids)}', (7, 65), bg_color=(0, 0, 0), text_color=(0, 255, 0))
            draw_text_with_background(annotated_frame, f'Left Street Cars: {len(current_region1_ids)}', (7, 105), bg_color=(255, 0, 0))
            draw_text_with_background(annotated_frame, f'Right Street Cars: {len(current_region2_ids)}', (880, 105), bg_color=(0, 255, 0))

            draw_text_with_background(annotated_frame, f'Road Condition: {"heavy" if len(current_region1_ids) > 2 else "smooth"}', (7, 139), bg_color=(255, 0, 0))
            draw_text_with_background(annotated_frame, f'Road Condition: {"heavy" if len(current_region2_ids) > 2 else "smooth"}', (880, 139), bg_color=(0, 255, 0))

            out.write(annotated_frame)

        cap.release()
        out.release()
