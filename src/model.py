"""Simple wrapper for loading a pre-trained object detection network.

We use OpenCV's DNN module with a MobileNet SSD that has been trained on the COCO
(or Pascal VOC) dataset. This file is intentionally written in a clear, step-by-step
way so a student can understand what's happening.
"""

import cv2

# paths to the model files; you need to download these and place them in the project
PROTO_TXT = "MobileNetSSD_deploy.prototxt.txt"
WEIGHTS = "MobileNetSSD_deploy.caffemodel"

# list of object categories that the network was trained on
# we've included only a subset for simplicity
CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]


def load_network():
    """Load the DNN model from disk and return the network object.

    The model uses the Caffe framework, but OpenCV hides those details.
    The prototxt file describes the architecture and the caffemodel file stores
    the weights. When you're a student, sometimes it's easier to re-download these
    than to train a new model from scratch.
    """
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(PROTO_TXT, WEIGHTS)
    print("[INFO] model loaded")
    return net


def preprocess_frame(frame):
    """Convert a video frame into a blob that the network understands.

    The network expects a 300x300 image and some mean subtraction. This function
    does that in a straightforward way using OpenCV helpers.
    """
    # the network was trained on images resized to 300x300
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    return blob
