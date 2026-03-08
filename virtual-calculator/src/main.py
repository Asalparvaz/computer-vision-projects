import cv2
import hand_tracker_module as htm

cap = cv2.VideoCapture(1)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)


    cv2.imshow("Virtual Calc", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break