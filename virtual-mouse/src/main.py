import cv2
import numpy as np
import time
import autopy

import hand_tracker_module as htm

detector = htm.HandDetector(detectionCon=0.7)

wcam, hcam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wcam)
cap.set(4, hcam)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)

    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()