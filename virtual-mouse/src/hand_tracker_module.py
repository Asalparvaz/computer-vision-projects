import cv2
import mediapipe as mp
import math

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, handNo=0):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])

        return self.lmList

    def get_hand_type(self):
        hand_types = []
        if self.results.multi_handedness:
            for hand in self.results.multi_handedness:
                hand_types.append(hand.classification[0].label)
        return hand_types

    def is_thumb_up(self):
        hand_types = self.get_hand_type()
        hand_type = hand_types[0] if hand_types else "Left"

        thumb_tip = self.lmList[4]
        thumb_ip = self.lmList[3]
        thumb_mcp = self.lmList[2]
        wrist = self.lmList[0]

        if hand_type == "Right":
            horizontal_check = thumb_tip[0] > thumb_ip[0]
        else:
            horizontal_check = thumb_tip[0] < thumb_ip[0]

        # Thumb tip is above thumb IP
        vertical_check = thumb_tip[1] < thumb_ip[1] < thumb_mcp[1]

        # Thumb tip is not too close to palm
        distance_to_palm = math.sqrt((thumb_tip[0] - wrist[0]) ** 2 + (thumb_tip[1] - wrist[1]) ** 2)
        palm_distance_check = distance_to_palm > 50

        return int(horizontal_check and vertical_check and palm_distance_check)


    def fingers_up(self):
        fingers = []

        if len(self.lmList) < 21:
            return fingers

        # THUMB
        fingers.append(self.is_thumb_up())


        # INDEX FINGER
        if self.lmList[8][2] < self.lmList[6][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # MIDDLE FINGER
        if self.lmList[12][2] < self.lmList[10][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # RING FINGER
        if self.lmList[16][2] < self.lmList[14][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # PINKY
        if self.lmList[20][2] < self.lmList[18][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        return fingers  # Returns [thumb, index, middle, ring, pinky]


    def find_distance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 255, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (255, 255, 255), cv2.FILLED)

        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        return length, img, [x1, y1, x2, y2, cx, cy]

    def get_bounding_box(self, img, handNo: int = 0, draw=True):
        if len(self.lmList) < 21:
            return None

        x_coords = [point[1] for point in self.lmList]
        y_coords = [point[2] for point in self.lmList]

        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        padding = 20

        if draw:
            cv2.rectangle(img, (x_min - padding, y_min - padding) ,
                          (x_max + padding, y_max + padding), (255, 255, 255), 2)

        return (x_min - padding, y_min - padding,
                x_max + padding, y_max + padding)