import cv2
import mediapipe as mp
import pyautogui
import pickle
import numpy as np
import json
import time
import os
import sys
from utils.smoother import CursorSmoother
from utils.voice import VoiceController

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(*parts):
    external_path = os.path.join(BASE_DIR, *parts)
    if os.path.exists(external_path):
        return external_path

    bundle_dir = getattr(sys, "_MEIPASS", BASE_DIR)
    return os.path.join(bundle_dir, *parts)


def output_path(*parts):
    return os.path.join(BASE_DIR, *parts)


os.chdir(BASE_DIR)

# load config
with open(resource_path("config.json"), encoding="utf-8") as f:
    config = json.load(f)

# load model
with open(resource_path("models", "gesture_model.pkl"), "rb") as f:
    model, le = pickle.load(f)

# setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils
smoother = CursorSmoother(r=config["kalman_r"], q=config["kalman_q"], dead_zone=config["dead_zone"])

screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(config["camera_index"])
if not cap.isOpened():
    raise RuntimeError(f"Could not open camera index {config['camera_index']}")

last_action_time = 0
is_dragging = False
margin = 0.15

# start voice controller in background
voice = VoiceController()
voice.start()
print("Voice control started! Try saying 'search youtube'")

def predict_gesture(lm):
    features = np.array([[v for p in lm for v in (p.x, p.y, p.z)]])
    pred = model.predict(features)[0]
    confidence = model.predict_proba(features).max()
    if confidence < config["confidence_threshold"]:
        return "unknown", confidence
    return le.inverse_transform([pred])[0], confidence

print("Gesture Mouse running! Press Q to quit.")

try:
    while True:
        success, frame = cap.read()
        if not success or frame is None:
            print("Could not read from camera. Exiting.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        gesture = "none"
        confidence = 0.0

        if result.multi_hand_landmarks:
            lm = result.multi_hand_landmarks[0].landmark
            mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

            gesture, confidence = predict_gesture(lm)
            now = time.time()
            cooldown_ok = (now - last_action_time) > config["click_cooldown"]

            # map webcam frame to screen with margin compensation
            x_norm = (lm[8].x - margin) / (1 - 2 * margin)
            y_norm = (lm[8].y - margin) / (1 - 2 * margin)

            # clamp between 0 and 1
            x_norm = max(0, min(1, x_norm))
            y_norm = max(0, min(1, y_norm))

            raw_x = int(x_norm * screen_w)
            raw_y = int(y_norm * screen_h)
            sx, sy = smoother.smooth(raw_x, raw_y)

            if gesture == "move":
                pyautogui.moveTo(sx, sy)

            elif gesture == "click" and cooldown_ok:
                pyautogui.click()
                last_action_time = now

            elif gesture == "right_click" and cooldown_ok:
                pyautogui.rightClick()
                last_action_time = now

            elif gesture == "scroll_up":
                pyautogui.scroll(config["scroll_speed"])

            elif gesture == "scroll_down":
                pyautogui.scroll(-config["scroll_speed"])

            elif gesture == "drag" and not is_dragging:
                pyautogui.mouseDown()
                is_dragging = True

            elif gesture == "screenshot" and cooldown_ok:
                screenshot_dir = output_path("screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                path = os.path.join(screenshot_dir, f"shot_{int(now)}.png")
                pyautogui.screenshot(path)
                print(f"Screenshot saved: {path}")
                last_action_time = now

            elif gesture == "freeze" and is_dragging:
                pyautogui.mouseUp()
                is_dragging = False

        # overlay
        color = (0, 255, 0) if confidence > config["confidence_threshold"] else (0, 165, 255)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Confidence: {confidence:.0%}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, "Voice: ON", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Gesture Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    if is_dragging:
        pyautogui.mouseUp()

    voice.stop()
    cap.release()
    cv2.destroyAllWindows()
