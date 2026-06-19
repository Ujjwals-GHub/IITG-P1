# 🦯 Shravan — Real-Time Object Detection & Voice Guidance System


A real-time assistive system designed to help visually impaired individuals navigate indoor environments. The system uses a custom-trained **YOLO** model designed over **YOLO11n** to detect household objects from a live webcam feed and announces their **position (left / ahead / right)** via text-to-speech.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Detected Object Classes](#-detected-object-classes)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Training the Model](#training-the-model)
  - [Running the Assistant](#running-the-assistant)
- [Configuration](#-configuration)
- [How It Works](#-how-it-works)
- [Known Limitations](#-known-limitations)

---

## 🔍 Overview

This project was developed as **Term Project 1** for the IIT Guwahati course/internship. It combines computer vision and speech synthesis to create a low-latency assistive tool that:

1. Captures a live video stream from a webcam.
2. Runs object detection using a fine-tuned YOLO model.
3. Determines whether each detected obstacle is to the **left**, **ahead**, or **right** of the user.
4. Speaks out a natural-language warning (e.g., *"chair left, table ahead"*) using Windows SAPI TTS.

---

## ✨ Features

- 🎥 **Real-time detection** — processes each frame from the webcam with bounding boxes and confidence scores.
- 🔊 **Voice alerts** — announces detected obstacles and their direction using Windows Speech API.
- 🧠 **Custom YOLO model** — trained on 13 indoor object classes relevant to home navigation.
- ⚡ **Duplicate suppression** — avoids repeating the same message within a configurable delay window.

---

## 📁 Project Structure

```
IITG-P1-main/
├── datasets/
│   ├── images/
│   │   ├── train/          # Training images
│   │   └── val/            # Validation images
│   └── labels/             # YOLO-format annotation .txt files
│   │   ├── train/          # Training labels
│   │   └── val/            # Validation labels
├── runs/
│   └── detect/             # Training run outputs (weights, metrics, plots)
├── model.yaml              # Dataset config for YOLO training
├── train_model.py          # Script to train the YOLO model
├── shravan.py              # Main script for launching assistant
├── yolo11n.pt              # Pre-trained YOLOv11 nano base weights
└── yolo26n.pt              # Alternative pre-trained YOLO weights
```

---

## 🏷️ Detected Object Classes

The model is trained to detect **13 indoor object classes**:

| ID | Class         | ID | Class         |
|----|---------------|----|---------------|
| 0  | Bed           | 7  | Wardrobe      |
| 1  | Sofa          | 8  | Window        |
| 2  | Chair         | 9  | Door          |
| 3  | Table         | 10 | Potted Plant  |
| 4  | Lamp          | 11 | Photo Frame   |
| 5  | TV            | 12 | Person        |
| 6  | Laptop        |    |               |

> **Dangerous / Alert-triggering objects** (subset used for voice warnings):
> `bed`, `chair`, `table`, `laptop`, `window`, `door`, `person`

---

## 🛠️ Requirements

- **OS:** Windows
- **Python:** 3.8+
- **Hardware:** Webcam, GPU recommended for real-time inference

### Python Dependencies

```
ultralytics       # YOLOv11 framework
opencv-python     # Webcam capture & frame rendering
pywin32           # Windows SAPI text-to-speech (win32com)
```

---

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/IITG-P1.git
   cd IITG-P1
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirement.txt
   ```

3. **Prepare the dataset** (if training from scratch)

   Place your images in `datasets/images/train/` and `datasets/images/val/`, and corresponding YOLO-format `.txt` label files in `datasets/labels/`.

---

## 💻 Usage

### Training the Model

```bash
python train_model.py
```

This will:
- Load the `yolo11n.pt` base weights.
- Train for **100 epochs** at image size **640×640**.
- Save weights and results under `runs/detect/`.

After training, update the model path in `shravan.py` to point to the best checkpoint:

```python
# shravan.py — line 9
model = YOLO(r"runs\detect\train<N>\weights\best.pt")
```

### Running the Assistant

```bash
python shravan.py
```

- A window titled **"Shravan"** will open showing the live webcam feed with bounding boxes.
- Detected obstacles will be announced via speakers.
- Press **`Q`** or **`ESC`** to quit.

---

## ⚙️ Configuration

You can tune the following constants in [`shravan.py`](shravan.py):

| Variable            | Default | Description                                              |
|---------------------|---------|----------------------------------------------------------|
| `CONF_THRESHOLD`    | `0.5`   | Minimum confidence score to trigger a detection          |
| `DELAY`             | `1`     | Minimum seconds between repeated identical announcements |
| `DANGEROUS_OBJECTS` | (list)  | Objects that trigger voice alerts                        |
| `speaker.Rate`      | `-1`    | TTS speaking rate (negative = slower)                    |

---

## ⚙️ How It Works

```
Webcam Frame
     │
     ▼
YOLO Inference  ──►  Filter by confidence & class
     │
     ▼
Direction Logic
  center_x < w/3  →  "left"
  center_x > 2w/3 →  "right"
  otherwise       →  "ahead"
     │
     ▼
Deduplicate messages  ──►  Speak via Windows SAPI TTS
     │
     ▼
Draw bounding boxes & display
```

---

## ⚠️ Known Limitations

- **Windows only** — the TTS engine uses `win32com` (Windows SAPI). Linux/macOS users would need to swap to `pyttsx3` or another TTS backend.
- **Poor Performance in Dark Rooms** — Webcam produces noisy frames in low light — more detections fall below the 50% confidence threshold
- **No depth estimation** — Direction is based solely on horizontal position; no distance information is provided.
- **No Object Tracking** - Each frame is processed independently — a fast-approaching person looks the same as a stationary one
- **Detection Scope** - model could only detect limited objects
- **Recall Gap** - 66.73% recall means 1 in 3 real objects are missed — more training data would improve this

---

## 🤝 Acknowledgements

- [Ultralytics YOLOv11](https://github.com/ultralytics/ultralytics) — object detection framework
- [OpenCV](https://opencv.org/) — video capture and rendering
- Developed as part of **IIT Guwahati Term Project 1**
