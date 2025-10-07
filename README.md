# 🚦 Traffic Congestion Detection using YOLOv11

## 🧠 Overview
This project implements a **real-time traffic congestion detection system** using **Computer Vision** and **Deep Learning**.  
The system detects vehicles in video feeds, tracks their movement across frames, and estimates congestion levels — **Smooth, Moderate, or Heavy** — using **YOLOv11** and **OpenCV**.

The goal is to help in **smart city traffic monitoring** and **automated congestion analysis**.

---

## 🎯 Objectives
- Detect vehicles in traffic images and videos.  
- Track vehicle movements across consecutive frames.  
- Estimate congestion level based on total vehicle count.  
- Provide annotated video output with bounding boxes, unique IDs, and congestion information.

---

## 🧩 Computer Vision Techniques Used
- **YOLOv11 Object Detection** – detects vehicles in each frame.  
- **OpenCV** – used for image overlays, bounding boxes, and real-time video rendering.  
- **BoT-SORT / ByteTrack** – advanced multi-object tracking algorithms that assign unique IDs to vehicles across frames.  
- **Polygon-based ROI** – region-of-interest analysis for lane-level congestion detection.  
- **Congestion Estimation** – logic based on vehicle count thresholds.

---

## 🗂️ Project Structure
```
Traffic_Congestion_Detection/
│
├── yolo_processor.py                # Main YOLO + tracking logic
├── Traffic_Congestion_Detection.ipynb  # Training & experimentation notebook
├── requirements.txt                 # Python dependencies
├── videos/                          # Input traffic videos
├── outputs/                         # Annotated output videos
├── runs/                            # YOLOv11 training results
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/J-Praveenan/Traffic-Congestion-Detection.git
cd Traffic-Congestion-Detection
```

### 2️⃣ Create Virtual Environment (optional)
```bash
python -m venv venv
# Activate environment
venv\Scripts\activate      # For Windows
source venv/bin/activate   # For Mac/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Download or Train YOLOv11 Model
You can use a pretrained YOLOv11 model:
```python
from ultralytics import YOLO
model = YOLO("yolov11n.pt")  # or yolov11s.pt
```

Or train your own model using:
```bash
yolo detect train data=data.yaml model=yolov11n.pt epochs=100 imgsz=640
```

### 5️⃣ Run the Video Detection Script
Edit paths in the code:
```python
video_path = "videos/input.mp4"
output_path = "outputs/result.mp4"
model_path = "yolov11n.pt"
```

Then execute:
```bash
python yolo_processor.py
```

---

## 🧪 Dataset & Training
- **Dataset**: Custom dataset of traffic images/videos.  
- **Total Images**: 536 training and 90 validation images.  
- **Annotation Tool**: LabelImg or Roboflow used to mark bounding boxes.  
- **Model**: YOLOv11 trained on GPU using the Ultralytics framework.  
- **Performance**:
  - **mAP@50** = 0.98 (98%)  
  - **mAP@50-95** = 0.74 (74%)  
  - **FPS** ≈ 30 (real-time inference)

---

## 📉 Training Results

### Training Accuracy Metrics
- **mAP@50** → Measures detection quality at 50% overlap (IoU).  
- **mAP@50–95** → Stricter metric averaged from 50% to 95% IoU.  
- High values indicate reliable detection and bounding-box precision.

### Training Loss Metrics
- **Box Loss** → Measures how accurately bounding boxes fit vehicles.  
- **Class Loss** → Ensures correct classification of detected objects.  
- **DFL Loss** → Distribution Focal Loss, improves box precision.

All loss curves **decrease steadily**, confirming the model is learning effectively.

---

## 📊 Results Summary
| Metric | Value |
|--------|--------|
| mAP@50 | **0.98 (98%)** |
| mAP@50–95 | **0.74 (74%)** |
| FPS (on GPU) | **~30 FPS** |
| Model | YOLOv11s |
| Dataset | 626 total images |

✅ **Inference Output**
- Vehicle detection with bounding boxes and confidence scores.  
- Unique tracking IDs assigned to each vehicle.  
- Total vehicle count and congestion status displayed on video.

---

## 🚦 Congestion Estimation Sample Logic
| Traffic Level | Condition |
|----------------|------------|
| **Heavy** | Vehicles ≥ 8 |
| **Moderate** | Vehicles ≥ 5 |
| **Smooth** | Vehicles < 5 |

The system counts vehicles in each frame and determines the road condition based on the provided threshold values.

---

## 🧑‍💻 Tech Stack
- **Python**
- **OpenCV**
- **Ultralytics YOLOv11**
- **NumPy**
- **BoT-SORT / ByteTrack**

---

## 🚀 Future Improvements
- Detect multiple vehicle types (cars, buses, bikes, trucks).  
- Integrate live CCTV camera feeds.  
- Deploy as a **real-time web app** or **cloud dashboard**.  
- Connect with smart traffic light control systems.

---

## 🏁 Conclusion
We successfully developed a **Traffic Congestion Detection System** capable of detecting and tracking vehicles in real time and classifying road conditions based on vehicle density.  
With further development, it can be integrated into **smart city traffic management systems** for automated decision-making.

---

## 📝 Acknowledgements
- **Ultralytics YOLOv11** – for model framework.  
- **OpenCV** – for image and video processing.  
- **BoT-SORT & ByteTrack** – for tracking algorithms.  


