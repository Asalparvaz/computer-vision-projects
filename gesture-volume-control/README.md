# 🔉 Gesture Volume Control
![Python 3.10](https://img.shields.io/badge/python-3.10-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green)
![Pycaw](https://img.shields.io/badge/Pycaw-20230407-orange)

Control your system volume using hand gestures in real-time.

This project uses MediaPipe hand tracking to measure the distance between the thumb and index finger and maps that distance to the system’s master volume level.  
It also supports gesture-based mute/unmute, a hold feature, and an on-screen UI for feedback.

## Features 🎯
- Hand gesture volume control (thumb & index distance)  
- Gesture-based mute/unmute (peace sign detection)  
- Hold volume (ASL ILY gesture detection)  
- Cooldown and edge-detection for gestures  
- On-screen volume bar with color feedback  
- Mute and hold icon indicators  

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
- Make a peace sign → toggle mute/unmute  
- Placement of the thumb is not important  
- Volume restores on unmute  
- Visual icon feedback on screen  

> **Peace Sign Visual Description:** ✌️   
> - **Index finger:** up  
> - **Middle finger:** up  
> - **Ring finger:** down  
> - **Pinky:** down  
> - **Thumb:** not important 

### Hold Gesture
- Make the ASL ILY sign → hold current volume  
- While in hold, volume cannot change from gestures until gesture is released  
- Visual lock icon on screen indicates hold state  

> **ASL ILY Sign Visual Description:** 🤟  
> - **Index finger:** up  
> - **Middle finger:** down  
> - **Ring finger:** down  
> - **Pinky:** up  
> - **Thumb:** up  

## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Gesture logic:
   - Volume control (distance between thumb and index)  
   - Mute toggle (peace sign, thumb placement not important)  
   - Hold (ASL ILY gesture)  
4. Volume is mapped to system audio range  
5. UI module renders:
   - Volume bar  
   - Mute icon  
   - Hold icon  
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