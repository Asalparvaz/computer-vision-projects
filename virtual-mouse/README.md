# 🖱️ Virtual Gesture Mouse
![Python 3.10](https://img.shields.io/badge/python-3.10-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0-green)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-orange)

Control your mouse cursor using hand gestures in real-time.

This project uses MediaPipe hand tracking to detect finger positions from your webcam.  
You can move the mouse, left click, right click, drag, and scroll — all without touching your physical mouse!

## Features 🎯

- Real-time hand tracking (21 landmarks)  
- Cursor movement using index finger  
- Left click gesture (index + middle pinch)  
- Double click gesture (index + middle double pinch)  
- Right click gesture (index + middle + ring pinch)  
- Drag & drop gesture (index + thumb pinch)  
- Scroll gesture (index + pinky movement)  
- Frame cropping for better control precision  
- Cursor smoothening to reduce jitter  
- Gesture cooldown to prevent accidental multi-click  
- YAML-based configuration system with fallback and dynamic screen detection  


## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Hand%20gestures/Pinching%20Hand.png" alt="Pinching Hand" width="25" height="25" /> Demo Concept

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

### Drag & Drop
- Raise **index + thumb**
- Pinch fingers close → hold (mouse down)
- Move hand to drag
- Release pinch → drop (mouse up)

### Scroll
- Raise **index + pinky**
- Move hand up or down
- Distance movement controls scroll direction and speed


| Finger | Movement☝️ | Left Click ✌️ | Right Click ✋ | Drag 🤏 | Scroll 🖐️ |
|--------|------------|--------------|--------------|--------|-----------|
| **Thumb** | down | down | down | up | down |
| **Index** | up | up | up | up | up |
| **Middle** | down | up | up | down | down |
| **Ring** | down | down | up | down | down |
| **Pinky** | down | down | down | down | up |
| **Notes** | — | Pinch triggers click<br>Double pinch → double click | Pinch triggers right click | Pinch holds mouse down | Vertical motion triggers scroll |


## 🔍 How It Works

1. Webcam captures live video using OpenCV  
2. MediaPipe detects 21 hand landmarks  
3. Finger states are calculated using landmark positions  
4. Gesture logic determines:
   - Movement mode  
   - Left click / double click  
   - Right click  
   - Drag & drop  
   - Scroll  
5. Cursor coordinates are mapped from camera space → screen space  
6. PyAutoGUI moves or clicks the system mouse  


## 🛠 Tech Stack

- **Python 3.10**
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI   
- PyYAML    

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


## ⚙️ Configuration

The project uses a YAML-based configuration system.    

- `config.yaml` → user-defined configuration    
- `config.example.yaml` → fallback configuration    
- If neither exists → hardcoded defaults are used     
- Screen resolution is auto-detected if width/height is set to `null`    


## 💡 Possible Improvements

- Horizontal scrolling
- GUI settings panel
- Gesture customization support  

---
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Camera%20with%20Flash.png" alt="Camera with Flash" width="25" height="25" /> Built for experimenting with computer vision and human-computer interaction.
