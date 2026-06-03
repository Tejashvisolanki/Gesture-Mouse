# 🖱️ Gesture Mouse

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightblue.svg)](https://www.microsoft.com/windows)

A powerful Python application that transforms hand gestures and voice commands into mouse, keyboard, and system actions using **MediaPipe** hand tracking and machine learning.

## ✨ Features

- 🖐️ **Hand Gesture Recognition** - Real-time hand tracking with MediaPipe + scikit-learn classifier
- 🎤 **Voice Commands** - Background voice control (search, click, scroll, type, copy/paste)
- 🖱️ **Mouse Control** - Move, click, right-click, scroll, drag, and freeze gestures
- 📸 **Screenshots** - Capture screenshots with hand gestures
- ✨ **Cursor Smoothing** - Kalman filter for smooth cursor movement
- 🎯 **Configurable Gestures** - Customize gesture names and parameters in `config.json`
- 💾 **Model Training** - Train custom gesture models with your own data

## 🚀 Quick Start

### Prerequisites
- Windows OS
- Python 3.11+ (MediaPipe compatibility)
- Webcam

### Installation

```bash
# Clone the repository
git clone https://github.com/Tejashvisolanki/Gesture-Mouse.git
cd Gesture-Mouse

# Create virtual environment
py -3.11 -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Note: If PyAudio fails
pipwin install pyaudio
```

### Train Model (First Run)

```bash
# Collect gesture samples
python collect_data.py

# Train the classifier
python train_model.py
```

### Run Application

```bash
python main.py
```

Press **`Q`** in the camera window to exit.

## 📁 Project Structure

```
├── main.py                      # Main gesture mouse application
├── tray.py                      # System tray launcher
├── collect_data.py              # Gesture data collector
├── train_model.py               # Model trainer
├── config.json                  # Configuration & gesture names
├── requirements.txt             # Python dependencies
├── utils/
│   ├── smoother.py             # Kalman filter cursor smoothing
│   └── voice.py                # Voice command handler
└── models/
    └── gesture_model.pkl       # Trained model (generated)
```

## 🎮 Available Gestures

| Gesture | Action |
|---------|--------|
| Move | Mouse movement |
| Click | Left click |
| Right Click | Right click |
| Scroll Up | Scroll up |
| Scroll Down | Scroll down |
| Drag | Start drag operation |
| Freeze | End drag operation |
| Screenshot | Capture screenshot |

## 🎙️ Voice Commands

- "Search YouTube" - Open YouTube search
- "Click" - Perform click
- "Scroll up/down" - Scroll
- And many more customizable commands!

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "camera_index": 0,              // Webcam index
  "confidence_threshold": 0.85,   // Gesture confidence
  "click_cooldown": 0.3,          // Minimum time between clicks
  "scroll_speed": 5,              // Scroll speed
  "kalman_r": 10,                 // Kalman filter R parameter
  "kalman_q": 0.1                 // Kalman filter Q parameter
}
```

## 🔨 Build Executable

```bash
# Build standalone executables
pyinstaller GestureMouseCore.spec
pyinstaller GestureMouse.spec
```

## 📊 Technology Stack

- **MediaPipe** - Hand pose detection
- **OpenCV** - Real-time video capture
- **scikit-learn** - Gesture classification
- **PyAudio** - Voice input
- **Kalman Filter** - Cursor smoothing

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

**Tejashvi Solanki** - [GitHub](https://github.com/Tejashvisolanki)

---

⭐ If you find this project helpful, please consider starring it!
