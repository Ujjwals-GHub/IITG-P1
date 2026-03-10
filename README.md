# Object Detection Assistant for the Visually Impaired

## Structure

```
project/
└── src/
    ├── model.py        # helper to load DNN model
    ├── detector.py     # functions to perform detection
    └── main.py         # run the camera loop and speak warnings
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the system:
   ```bash
   python src/main.py
   ```

## Acknowledgements
The object detection model is based on MobileNet SSD and COCO classes.

