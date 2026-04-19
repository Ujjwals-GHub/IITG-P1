import cv2
from ultralytics import YOLO
import win32com.client
import time

# ======================
# LOAD MODEL
# ======================
#model = YOLO(r"C:\Users\ujjwa\Desktop\project\3rd\runs\detect\train6\weights\best.pt")
model = YOLO(r"C:\Users\ujjwa\Desktop\project\3rd\runscol\detect\train3\weights\best.pt")

cap = cv2.VideoCapture(0)

# ======================
# SETTINGS
# ======================
CONF_THRESHOLD = 0.5
DELAY = 1  # seconds

DANGEROUS_OBJECTS = ["bed", "chair", "table", "laptop", "window", "door", "person"]

last_spoken_time = 0
last_message = ""

# ======================
# TTS ENGINE (KEEP ONE INSTANCE)
# ======================
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = -1  # Slower rate

def speak(text):
    speaker.Speak(text)

# ======================
# MAIN LOOP
# ======================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    h, w, _ = frame.shape
    messages = []

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])
            if conf < CONF_THRESHOLD:
                continue

            cls = int(box.cls[0])
            label = model.names[cls]

            if label not in DANGEROUS_OBJECTS:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            center_x = (x1 + x2) // 2

            # Direction logic
            if center_x < w // 3:
                direction = "left"
            elif center_x > 2 * w // 3:
                direction = "right"
            else:
                direction = "ahead"

            messages.append(f"{label} {direction}")

            # Draw
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0,255,0), 2)

    # ======================
    # SPEAK LOGIC (FIXED)
    # ======================
    current_time = time.time()

    if messages:
        unique_msg = ", ".join(sorted(set(messages)))

    
        if (unique_msg != last_message) or (current_time - last_spoken_time > DELAY):
            print("[SPEAK]", unique_msg)
            speak(unique_msg)

            last_message = unique_msg
            last_spoken_time = current_time

    # ======================
    # SHOW
    # ======================
    cv2.imshow("Blind Assistant", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()