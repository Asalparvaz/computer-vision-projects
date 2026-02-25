import cv2
import numpy as np
import time
import autopy

import hand_tracker_module as htm

detector = htm.HandDetector(maxHands=1)

wscreen, hscreen = autopy.screen.size()
wcam, hcam = 640, 480
frameR = 100 # Frame Reduction

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
    bbox = detector.get_bounding_box(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # index finger
        x2, y2 = lmList[12][1:] # middle finger

        fingers = detector.fingers_up()

        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (0, 0, 255), 2)

        if fingers[1] and not fingers[2]:
            # moving mode

            x3 = np.interp(x1, (frameR, wcam-frameR), (0, wscreen))
            y3 = np.interp(y1, (frameR, hcam-frameR), (0, hscreen))

            autopy.mouse.move(x3, y3)
            cv2.circle(img, (x1,y1), 15, (0, 0, 255), cv2.FILLED)


        if fingers[1] and fingers[2]:
            # clicking mode

            length, img, line_info = detector.find_distance(8, 12, img)

            if length < 40:
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()


    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()