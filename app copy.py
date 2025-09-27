from flask import Flask, request, jsonify, send_file
import os
import uuid
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask_cors import CORS
from yolo_processor import YOLOVideoProcessor


app = Flask(__name__)
CORS(app) 
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/detect', methods=['POST'])
def detect_traffic():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = f"{uuid.uuid4()}.mp4"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"result_{filename}")

    file.save(input_path)

    processor = YOLOVideoProcessor(
        model_path="models/best.pt",  # <-- path to your model
        video_path=input_path,
        output_path=output_path,
        tracker_method="bot",
        classes=[0]
    )
    processor.process_video()

    return send_file(output_path, mimetype="video/mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
