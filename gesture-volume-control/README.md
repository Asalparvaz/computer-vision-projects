# 🔉 Gesture Volume Control

Control your system volume using hand gestures in real-time.

This project uses MediaPipe hand tracking to measure the distance between the thumb and index finger and maps that distance to the system’s master volume level.


## 🎯 Demo Concept

- Bring thumb and index finger closer → lower volume  
- Move them apart → increase volume  
- Volume percentage is displayed on screen  
- Color feedback:
  - 🔴 Very low (0-5%)
  - 🟢 Very high (95-100%)
  - ⚪ Neutral range  


## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Thumb tip (id 4) and index tip (id 8) positions are extracted  
4. Euclidean distance is calculated  
5. Distance is interpolated to the system volume range  
6. Volume updates in real-time  


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
python main.py
```

## 💡 Possible Improvements

- Add smoothing to reduce jitter  
- Add on-screen volume bar  
- Dynamic calibration for different hand sizes  
- Gesture-based mute toggle