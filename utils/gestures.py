import pyautogui
import time

class GestureHandler:
    def __init__(self, config):
        self.config = config
        self.last_action_time = 0
        self.is_dragging = False

    def cooldown_ok(self):
        return (time.time() - self.last_action_time) > self.config["click_cooldown"]

    def handle(self, gesture, sx, sy, smoother):
        now = time.time()

        if gesture == "move":
            pyautogui.moveTo(sx, sy)

        elif gesture == "click" and self.cooldown_ok():
            pyautogui.click()
            self.last_action_time = now

        elif gesture == "right_click" and self.cooldown_ok():
            pyautogui.rightClick()
            self.last_action_time = now

        elif gesture == "scroll_up":
            pyautogui.scroll(self.config["scroll_speed"])

        elif gesture == "scroll_down":
            pyautogui.scroll(-self.config["scroll_speed"])

        elif gesture == "drag" and not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True

        elif gesture == "freeze" and self.is_dragging:
            pyautogui.mouseUp()
            self.is_dragging = False

        elif gesture == "screenshot" and self.cooldown_ok():
            import os
            os.makedirs("screenshots", exist_ok=True)
            path = f"screenshots/shot_{int(now)}.png"
            pyautogui.screenshot(path)
            print(f"Screenshot saved: {path}")
            self.last_action_time = now

    def cleanup(self):
        if self.is_dragging:
            pyautogui.mouseUp()