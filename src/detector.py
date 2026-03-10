"""Functions for running object detection on frames.

This module takes a network object (from model.py) and applies it to video frames.
It returns a list of detections where each detection is a tuple with the class name
and bounding box coordinates.
"""

import cv2
import numpy as np
from model import CLASSES


def detect_objects(net, frame, confidence_threshold=0.2):
    """Run the network on a frame and collect detections.

    Parameters:
        net: the pre-loaded DNN network
        frame: a single image (numpy array) from a video stream
        confidence_threshold: filter out weak detections

    Returns:
        detections: a list of (class_label, confidence, box) tuples
                    where box=(startX, startY, endX, endY)
    """
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    results = []
    # loop over the detections and filter by confidence
    for i in range(0, detections.shape[2]):
        conf = detections[0, 0, i, 2]
        if conf > confidence_threshold:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx] if idx < len(CLASSES) else "unknown"
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            results.append((label, conf, (startX, startY, endX, endY)))
    return results
