# 🖱️ Virtual Gesture Mouse
![Python 3.10](https://img.shields.io/badge/python-3.10-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green)
![Autopy](https://img.shields.io/badge/PyAutoGUI-0.9.54-orange)

Control your mouse cursor using hand gestures in real-time.

This project uses MediaPipe hand tracking to detect finger positions from your webcam.  
You can move the mouse, left click, and right click without touching your physical mouse!

## Features 🎯

- Real-time hand tracking (21 landmarks)
- Smooth cursor movement using index finger
- Left click gesture (index + middle pinch)
- Double click gesture (index + middle pinch twice)
- Right click gesture (index + middle + ring pinch)
- Frame cropping for better control precision
- Cursor smoothening to reduce jitter
- Gesture cooldown to prevent accidental multi-click
- On-screen visual feedback (bounding box, interaction frame)

## 🤏 Demo Concept

### Cursor Movement
- Raise **index finger only**
- Move your hand inside the red frame
- Cursor follows your index finger
- Smoothening reduces jitter for stable movement

### Left Click (& Double Click)
- Raise **index + middle fingers**
- Bring fingertips close together (pinch)
- When distance < threshold → left click
- Pinch your fingers twice for a double click

### Right Click
- Raise **index + middle + ring fingers**
- Bring index and middle fingertips close
- When distance < threshold → right click

| Finger | Movement Gesture ☝️ | Left Click Gesture ✌️ | Right Click Gesture ✋ |
|--------|-------------------|----------------------|-----------------------|
| **Index** | up | up | up |
| **Middle** | down | up | up |
| **Ring** | down | down | up |
| **Pinky** | down | down | down |
| **Thumb** | down | down | down |
| **Notes** | — | Pinch distance triggers click<br>Double pinch triggers double click | Pinch distance triggers click |


## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Finger states are calculated using landmark positions  
4. Gesture logic determines:
   - Movement mode  
   - Left click  
   - Right click  
5. Cursor coordinates are mapped from camera space → screen space  
6. Autopy moves or clicks the system mouse  


## 🛠 Tech Stack

- **Python 3.10**
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## ▶️ Run Locally

Install dependencies:    
```
pip install -r requirements.txt
```

Run:    
```
python src/main.py
```

Press `q` to exit.


## 💡 Possible Improvements

- Drag & drop gesture (pinch and hold)
- Scrolling
- Dynamic calibration for different screen sizes