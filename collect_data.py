import cv2
import mediapipe as mp
import csv
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

print("Available gestures:", config["gestures"])
GESTURE_LABEL = input("Enter gesture name to collect: ").strip()

if GESTURE_LABEL not in config["gestures"]:
    print(f"Unknown gesture! Add it to config.json first.")
    raise SystemExit(1)

cap = cv2.VideoCapture(config["camera_index"])
if not cap.isOpened():
    raise RuntimeError(f"Could not open camera index {config['camera_index']}")

count = 0
os.makedirs("data", exist_ok=True)

print(f"\nCollecting: '{GESTURE_LABEL}'")
print("Hold gesture -> press SPACE to capture -> press Q to quit\n")

try:
    while True:
        success, frame = cap.read()
        if not success or frame is None:
            print("Could not read from camera. Exiting.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        lm = None

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0].landmark
            mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            cv2.putText(frame, f"Gesture: {GESTURE_LABEL} | Samples: {count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No hand detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow(f"Collecting: {GESTURE_LABEL}", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        if key == ord(' ') and lm is not None:
            row = [GESTURE_LABEL] + [v for p in lm for v in (p.x, p.y, p.z)]
            with open("data/gestures.csv", "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(row)
            count += 1
            print(f"Captured sample {count}")
finally:
    cap.release()
    cv2.destroyAllWindows()
print(f"\nDone! Collected {count} samples for '{GESTURE_LABEL}'")
