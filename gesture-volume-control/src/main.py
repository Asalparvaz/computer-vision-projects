#TODAY'S TO-DO (mute option):
# 1. first fist -> mutes -> you can't do anything -> second fist -> unmute
# 2. track last volume, when it unmutes it goes to that
# 3. display when muted

import cv2
import numpy as np
import math

import hand_tracker_module as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

muted = False


color = (77, 77, 77)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)

    if len(lmList) != 0:

        handType = detector.get_hand_type()[0]
        is_fist = detector.is_fist(lmList, handType=handType)


        if is_fist: # Simple concept 
            muted=True
            volume.SetMasterVolumeLevel(minVol, None)
            print("Muted!")
        else :
            muted=False

        if not muted:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1+x2) // 2 , (y1+y2) // 2

            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            length = math.hypot(x2-x1, y2-y1)

            vol = np.interp(length, [20, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

            vol_percentage = np.interp(length, [20, 200], [0, 100])

            if vol_percentage < 5:
                color = (0, 0, 255)
            elif vol_percentage > 95:
                color = (0, 255, 0)
            else:
                color = (77, 77, 77)

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            display_x = cx
            display_y = cy

            cv2.putText(img, f"{int(vol_percentage)}%", (display_x, display_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)


    cv2.imshow("Volume Control", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()