# 🔉 Gesture Volume Control

Control your system volume using hand gestures in real-time.

This project uses MediaPipe hand tracking to measure the distance between the thumb and index finger and maps that distance to the system’s master volume level.   
It also supports gesture-based mute/unmute and an on-screen UI for feedback


## Features 🎯
- Hand gesture volume control (thumb & index distance)
- Gesture-based mute/unmute (fist detection)
- Cooldown and edge-detection for mute/unmute
- On-screen volume bar with color feedback
- Mute icon indicator

## 🤏 Demo Concept

### Volume Control
- Bring thumb and index finger closer → lower volume  
- Move them apart → increase volume  
- Volume percentage is displayed on screen

### Color Feedback
- 🔴 Very low (0-5%)
- 🟢 Very high (95-100%)
- ⚪ Neutral range

### Mute Gesture
- Make a fist -> toggle mute/unmute
- Volume restores on unmute (you can adjust it after a brief moment)
- Visual icon feedback on screen


## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Gesture logic:
   - Volume control (distance between thumb and index)
   - Mute toggle (fist)
4. Volume is mapped to system audio range
5. UI module renders:
   - Volume bar
   - Mute icon
   - Percentage feedback


## 🛠 Tech Stack

- **Python 3.10**  
- OpenCV  
- MediaPipe  
- NumPy  
- Pycaw (Windows audio control)  


## ▶️ Run Locally

Install dependencies:

```
pip install -r requirements.txt
```

Run:
```
python src/main.py
```

press `q` to exit.

## 💡 Possible Improvements

- Add smoothing to reduce jitter  
- Dynamic calibration for different hand sizes 