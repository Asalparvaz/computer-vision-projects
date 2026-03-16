# ⌨️ Virtual Keyboard

![Python 3.10](https://img.shields.io/badge/python-3.10-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green)

**Control your keyboard using hand gestures in real-time.**

This project uses MediaPipe hand tracking to detect finger positions from your webcam.  
You can type anything — without touching your physical keyboard!   

## Features 🎯

- Real-time hand tracking (21 landmarks)  
- Cursor movement using index finger  
- Hover animation and click feedback
- Gesture cooldown to prevent accidental multi-click  


## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Hand%20gestures/Pinching%20Hand.png" alt="Pinching Hand" width="25" height="25" /> Demo Concept

### Click buttons ✌️
- Raise **index + middle fingers**
- Move through the button with the hover feedback
- Bring fingertips close together (pinch)
- When distance < threshold → click
- Click is based on the middle of your fingertips    


## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Finger states are calculated using landmark positions  
4. Gesture logic determines click for a specific button    
5. Based on the location the button is found and pressed   

## 🛠️ Tech Stack

- **Python 3.10**
- OpenCV
- MediaPipe

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

- Type in any application on your device    
- Capital/small option (and Caps lock)   
- Add numbers and special characters   
- More functional buttons such as shift, control, ...  
- Support multiple languages (esp Persian)     

---
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Camera%20with%20Flash.png" alt="Camera with Flash" width="25" height="25" /> Built for experimenting with computer vision and input-output interaction.
