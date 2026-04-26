import speech_recognition as sr
import pyautogui
import threading
import webbrowser
import os
import subprocess
import time
from urllib.parse import quote_plus

class VoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_running = False
        self.thread = None

    def process_command(self, command):
        print(f"Voice command: {command}")

        if "open chrome" in command:
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    break
            else:
                webbrowser.open("https://www.google.com")

        elif "open notepad" in command:
            subprocess.Popen(["notepad.exe"])

        elif "open file explorer" in command:
            subprocess.Popen(["explorer.exe"])

        elif "open task manager" in command:
            subprocess.Popen(["taskmgr.exe"])

        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")

        elif "screenshot" in command:
            os.makedirs("screenshots", exist_ok=True)
            path = os.path.join("screenshots", f"voice_shot_{int(time.time())}.png")
            pyautogui.screenshot(path)
            print(f"Screenshot saved: {path}")

        elif "scroll up" in command:
            pyautogui.scroll(5)

        elif "scroll down" in command:
            pyautogui.scroll(-5)

        elif "right click" in command:
            pyautogui.rightClick()

        elif "click" in command:
            pyautogui.click()

        elif "press enter" in command:
            pyautogui.press("enter")

        elif "press escape" in command:
            pyautogui.press("escape")

        elif "press tab" in command:
            pyautogui.press("tab")

        elif "select all" in command:
            pyautogui.hotkey("ctrl", "a")

        elif "copy" in command:
            pyautogui.hotkey("ctrl", "c")

        elif "paste" in command:
            pyautogui.hotkey("ctrl", "v")

        elif "undo" in command:
            pyautogui.hotkey("ctrl", "z")

        elif "close window" in command:
            pyautogui.hotkey("alt", "f4")

        elif "minimize" in command:
            pyautogui.hotkey("win", "down")

        elif "maximize" in command:
            pyautogui.hotkey("win", "up")

        elif "stop" in command or "exit" in command:
            self.stop()

        elif "type" in command:
            text = command.replace("type", "").strip()
            pyautogui.typewrite(text, interval=0.05)

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Voice control active! Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                while self.is_running:
                    try:
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                        command = self.recognizer.recognize_google(audio).lower()
                        self.process_command(command)
                    except sr.WaitTimeoutError:
                        pass
                    except sr.UnknownValueError:
                        pass
                    except Exception as e:
                        print(f"Voice error: {e}")
        except Exception as e:
            self.is_running = False
            print(f"Voice control unavailable: {e}")

    def start(self):
        if self.is_running:
            return

        self.is_running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        print("Voice control stopped.")
