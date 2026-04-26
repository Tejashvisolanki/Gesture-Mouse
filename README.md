# GestureMouse

GestureMouse is a Windows-focused Python app that turns webcam hand gestures and voice commands into mouse, keyboard, scrolling, dragging, and screenshot actions.

## Features

- Hand gesture recognition with MediaPipe landmarks and a scikit-learn model
- Cursor smoothing with a Kalman filter
- Mouse movement, left click, right click, scroll, drag, freeze, and screenshot gestures
- Background voice commands for search, clicking, scrolling, typing, copy/paste, window control, and launching common apps
- Optional system tray launcher for packaged builds

## Project Structure

```text
main.py                  # Live gesture mouse app
tray.py                  # System tray launcher
collect_data.py          # Webcam gesture data collector
train_model.py           # Trains the gesture classifier
config.json              # Runtime settings and gesture names
data/gestures.csv        # Generated local training samples
models/gesture_model.pkl # Generated local model and label encoder
utils/                   # Gesture, smoothing, and voice helpers
```

## Setup

Use Python 3.11 or 3.12. Some webcam/ML dependencies, especially MediaPipe, may not have wheels for the newest Python releases.

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If `PyAudio` fails to install on Windows, install a compatible wheel or use:

```powershell
pip install pipwin
pipwin install pyaudio
```

## Run

Before first run, collect gesture samples and train the model so `models/gesture_model.pkl` exists.

```powershell
python main.py
```

Press `Q` in the OpenCV camera window to quit.

## Collect New Gesture Data

```powershell
python collect_data.py
```

Choose one of the gesture names from `config.json`, hold the gesture, press Space to save a sample, and press `Q` to quit.

## Train The Model

```powershell
python train_model.py
```

The trained model is saved to `models/gesture_model.pkl`.

Generated training artifacts are intentionally ignored by Git:

```text
data/gestures.csv
models/gesture_model.pkl
```

## Build Executables

Build after training, because `GestureMouseCore.spec` packages the locally generated model.

```powershell
pyinstaller GestureMouseCore.spec
pyinstaller GestureMouse.spec
```

The tray app launches the core gesture mouse executable.
