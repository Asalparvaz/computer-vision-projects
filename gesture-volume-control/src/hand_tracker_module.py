import cv2
import mediapipe as mp

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
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        return lmList

    def get_hand_type(self):
        hand_types = []
        if self.results.multi_handedness:
            for hand in self.results.multi_handedness:
                hand_types.append(hand.classification[0].label)
        return hand_types

    def is_fist(self, lmList, handType="right"):
        if len(lmList) == 0:
            return False

        # Thumb detection
        # location of the thumb tip related to the base of it
        if handType == "Right":
            thumb_curled = lmList[4][1] > lmList[3][1]
        else:
            thumb_curled = lmList[4][1] < lmList[3][1]

        # Other fingers
        fingers_curled = True
        for id in range(8, 21, 4):  # 8, 12, 16, 20
            if lmList[id][2] < lmList[id - 2][2]:  # If any tip is above middle joint
                fingers_curled = False
                break

        return thumb_curled and fingers_curled

    def is_hold(self, lmList):
        if len(lmList) < 21:
            return False

        index_up = lmList[8][2] < lmList[6][2]
        middle_up = lmList[12][2] < lmList[10][2]
        ring_up = lmList[16][2] < lmList[14][2]
        pinky_up = lmList[20][2] < lmList[18][2]

        return (index_up and pinky_up) and not (middle_up or ring_up)
