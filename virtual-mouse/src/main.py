import cv2
import numpy as np
import pyautogui
import time

import hand_tracker_module as htm

detector = htm.HandDetector(maxHands=1)

screen_width, screen_height = pyautogui.size()
camera_width, camera_height = 640, 480
horizontal_frame_crop = 100
top_frame_crop = 50
bottom_frame_crop = 150

smoothening = 3
ploc_x, ploc_y = 0, 0
cloc_x, cloc_y = 0, 0

CLICK_LENGTH_THRESHOLD = 30
DRAG_LENGTH_THRESHOLD = 90
CLICK_DELAY = 0.3
DOUBLE_CLICK_TIMEOUT = 0.4

last_click_time = 0
pending_double_click = False

SCROLL_SPEED = 100
SCROLL_DEADZONE = 20
SCROLL_COOLDOWN = 0.05
scroll_start_y = None
scroll_active = False
last_scroll_time = 0


is_dragging = False

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

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

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        fingers = detector.fingers_up()

        cv2.rectangle(img, (horizontal_frame_crop, top_frame_crop),
                      (camera_width - horizontal_frame_crop, camera_height - bottom_frame_crop), (0, 0, 255), 2)

        if fingers[1] and not (fingers[0] or fingers[2] or fingers[3] or fingers[4]):
            # moving mode
            x3 = np.interp(x1, (horizontal_frame_crop, camera_width - horizontal_frame_crop), (0, screen_width))
            y3 = np.interp(y1, (top_frame_crop, camera_height - bottom_frame_crop), (0, screen_height))

            cloc_x = ploc_x + (x3 - ploc_x) / smoothening
            cloc_y = ploc_y + (y3 - ploc_y) / smoothening

            pyautogui.moveTo(cloc_x, cloc_y)

            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            ploc_x, ploc_y = cloc_x, cloc_y

        if fingers[1] and fingers[2] and not (fingers[0] or fingers[3] or fingers[4]):
            # clicking mode LEFT
            current_time = time.time()

            length, img, line_info = detector.find_distance(8, 12, img)

            if length < CLICK_LENGTH_THRESHOLD:
                if (current_time - last_click_time) > CLICK_DELAY:
                    if pending_double_click and (current_time - last_click_time) <= DOUBLE_CLICK_TIMEOUT:
                        # Double click detected
                        pyautogui.doubleClick()
                        cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                        pending_double_click = False
                        last_click_time = current_time
                    else:
                        # First click or timeout done
                        pending_double_click = True
                        cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                        last_click_time = current_time

        if fingers[1] and fingers[2] and fingers[3] and not (fingers[0] or fingers[4]):
            # clicking mode RIGHT
            current_time = time.time()

            length, img, line_info = detector.find_distance(8, 12, img)

            if length < CLICK_LENGTH_THRESHOLD and (current_time - last_click_time) > CLICK_DELAY:
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.rightClick()
                last_click_time = current_time
                pending_double_click = False


        if fingers[1] and fingers[0] and not (fingers[2] or fingers[3] or fingers[4]):
            # drag mode
            length, img, line_info = detector.find_distance(8, 4, img)

            if length < DRAG_LENGTH_THRESHOLD:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True

                x3 = np.interp(x1, (horizontal_frame_crop, camera_width - horizontal_frame_crop), (0, screen_width))
                y3 = np.interp(y1, (top_frame_crop, camera_height - bottom_frame_crop), (0, screen_height))

                cloc_x = ploc_x + (x3 - ploc_x) / smoothening
                cloc_y = ploc_y + (y3 - ploc_y) / smoothening
                ploc_x, ploc_y = cloc_x, cloc_y

                pyautogui.moveTo(cloc_x, cloc_y)
                cv2.circle(img, (line_info[4], line_info[5]), 15, (0, 255, 255), cv2.FILLED)

            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False

        if not fingers[0] and is_dragging:
            is_dragging = False
            pyautogui.mouseUp()

        if fingers[1] and fingers[4] and not (fingers[0] or fingers[2] or fingers[3]) :
            # scroll mode
            current_time = time.time()
            x5, y5 = lmList[20][1:] # pinky tip

            if not scroll_active:
                scroll_active = True
                scroll_start_y = y1
            else:
                delta_y = scroll_start_y - y1

                if abs(delta_y) > SCROLL_DEADZONE and (current_time - last_click_time) > SCROLL_COOLDOWN:
                    scroll_amount = int(delta_y / SCROLL_DEADZONE * SCROLL_SPEED)

                    pyautogui.scroll(scroll_amount)

                    scroll_start_y = y1
                    last_scroll_time = current_time

            cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x5, y5), 15, (0, 255, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x5, y5), (0, 255, 255), 3)

        else:
            scroll_active = False
            scroll_start_y = None
        

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()