"""Main script: open camera, detect objects, and speak warnings.

This is the "user-facing" part of the project. When run, it will access the default
webcam, run the model on each frame, draw boxes for debugging, and use a text-to-speech
engine to warn the user.

The code is purposely not optimized for speed or size; clarity is the priority so a
student can follow along.
"""

import cv2
import pyttsx3

from model import load_network
from detector import detect_objects


def speak(text):
    """Say a string out loud. This uses the pyttsx3 engine which works offline."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():
    print("[INFO] starting video stream...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] cannot open camera")
        return

    net = load_network()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] failed to grab frame")
            break

        detections = detect_objects(net, frame)

        # simple logic: if any "person" or "chair" or "dog" etc. is close, warn
        warnings = set()
        for (label, conf, box) in detections:
            (startX, startY, endX, endY) = box
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = f"{label}: {conf:.2f}"
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            if label in ("person", "chair", "dog", "car", "bus", "bicycle"):
                warnings.add(label)

        # speak once per frame (could lead to repeated speech; student code keeps it simple)
        if warnings:
            phrase = "Warning, " + ", ".join(warnings) + " ahead."
            print("[SPEAK]", phrase)
            speak(phrase)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
