import cv2
import hand_tracker_module as htm
import button_module as btn

cap = cv2.VideoCapture(1)
cap.set(3, 1280) #width
cap.set(4, 720) #height

detector = htm.HandDetector(detectionCon=0.8)

button_test = btn.Button((100, 100),100, 100, 'Q')

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)

    button_test.draw(img)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break