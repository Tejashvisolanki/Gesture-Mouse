import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import sys
import os
import subprocess

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CORE_PROCESS = None

def find_core_exe():
    candidates = [
        os.path.join(BASE_DIR, "GestureMouseCore.exe"),
        os.path.join(BASE_DIR, "dist", "GestureMouseCore.exe"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return candidates[0]

def create_icon():
    img = Image.new("RGB", (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([16, 16, 48, 48], fill=(0, 255, 0))
    return img

def start_gesture_mouse(icon, item):
    global CORE_PROCESS

    if CORE_PROCESS is not None and CORE_PROCESS.poll() is None:
        return

    def run():
        global CORE_PROCESS

        core_exe = find_core_exe()
        if not os.path.exists(core_exe):
            icon.notify(f"Could not find {core_exe}", "Gesture Mouse")
            return

        CORE_PROCESS = subprocess.Popen([core_exe], cwd=os.path.dirname(core_exe))

    threading.Thread(target=run, daemon=True).start()

def stop_app(icon, item):
    global CORE_PROCESS

    if CORE_PROCESS is not None and CORE_PROCESS.poll() is None:
        CORE_PROCESS.terminate()
        try:
            CORE_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            CORE_PROCESS.kill()
            CORE_PROCESS.wait()

    icon.stop()
    sys.exit()

def run_tray():
    icon = pystray.Icon(
        "GestureMouse",
        create_icon(),
        "Gesture Mouse",
        menu=pystray.Menu(
            item("Start Gesture Mouse", start_gesture_mouse),
            item("Quit", stop_app)
        )
    )
    icon.run()

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    run_tray()
