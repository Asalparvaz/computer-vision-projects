import cv2
import numpy as np
import autopy

import hand_tracker_module as htm

detector = htm.HandDetector(maxHands=1)

screen_width, screen_height = autopy.screen.size()
camera_width, camera_height = 640, 480
horizontal_frame_crop = 100
top_frame_crop = 50
bottom_frame_crop = 150

smoothening = 3
ploc_x, ploc_y = 0, 0
cloc_x, cloc_y = 0, 0


cap = cv2.VideoCapture(1)
cap.set(3, camera_width)
cap.set(4, camera_height)

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

        cv2.rectangle(img, (horizontal_frame_crop, top_frame_crop),
                      (camera_width - horizontal_frame_crop, camera_height - bottom_frame_crop), (0, 0, 255), 2)

        if fingers[1] and not (fingers[2] or fingers[0]):
            # moving mode

            x3 = np.interp(x1, (horizontal_frame_crop, camera_width - horizontal_frame_crop), (0, screen_width))
            y3 = np.interp(y1, (top_frame_crop, camera_height - bottom_frame_crop), (0, screen_height))

            cloc_x = ploc_x + (x3 - ploc_x) / smoothening
            cloc_y = ploc_y + (y3 - ploc_y) / smoothening

            autopy.mouse.move(cloc_x, cloc_y)
            cv2.circle(img, (x1,y1), 15, (0, 0, 255), cv2.FILLED)
            ploc_x, ploc_y = cloc_x, cloc_y


        if fingers[1] and fingers[2] and not (fingers[0] or fingers[3] or fingers[4]):
            # clicking mode LEFT

            length, img, line_info = detector.find_distance(8, 12, img)

            if length < 30:
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        if fingers[1] and fingers[0] and not (fingers[2] or fingers[3] or fingers[4]):
            # clicking mode RIGHT

            length, img, line_info = detector.find_distance(8, 4, img)

            if length < 70:
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)


    cv2.imshow("Virtual Mouse", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()