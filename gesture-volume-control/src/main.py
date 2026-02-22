import cv2
import numpy as np
import math

import hand_tracker_module as htm
from ui import draw_ui

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

muted = False
mute_seen_prev = False
mute_cooldown = False
mute_cooldown_frames = 20
mute_frame_counter = 0

just_unmuted = False
unmute_delay_cooldown = 10
unmute_frame_counter = 0

last_volume = 0.0

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


        if is_fist and not mute_seen_prev and not mute_cooldown:
            if muted:
                muted=False
                just_unmuted = True
                volume.SetMasterVolumeLevelScalar(last_volume, None)
            else:
                muted = True
                mute_cooldown = True
                last_volume = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(0.0, None)

            mute_frame_counter = 0
            unmute_frame_counter = 0


        mute_seen_prev = is_fist

        if mute_cooldown:
            mute_frame_counter+=1
            if mute_frame_counter >= mute_cooldown_frames:
                mute_cooldown = False

        if just_unmuted:
            unmute_frame_counter+=1
            if unmute_frame_counter >= unmute_delay_cooldown:
                just_unmuted = False

        if not muted and not just_unmuted:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1+x2) // 2 , (y1+y2) // 2

            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            length = math.hypot(x2-x1, y2-y1)

            vol_scalar = np.interp(length, [20, 200], [0.0, 1.0])
            volume.SetMasterVolumeLevelScalar(vol_scalar, None)

            vol_percentage = vol_scalar * 100

            if vol_percentage < 5:
                color = (0, 0, 255)
            elif vol_percentage > 95:
                color = (0, 255, 0)
            else:
                color = (77, 77, 77)

    current_vol = volume.GetMasterVolumeLevelScalar()
    vol_percentage = current_vol * 100

    draw_ui(img, vol_percentage, muted)

    cv2.imshow("Volume Control", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()