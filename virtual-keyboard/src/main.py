import cv2
import hand_tracker_module as htm
import button_module as btn

cap = cv2.VideoCapture(1)
cap.set(3, 1280) #width
cap.set(4, 720) #height

detector = htm.HandDetector(detectionCon=0.8)

button_list = []

english_keyboard_value = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                          ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
                          ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

for y in range(len(english_keyboard_value)):
    for x, value in enumerate(english_keyboard_value[y]):
        button_list.append(btn.Button((100 * x + 50 , 100 * y + 50), value))

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)

    for button in button_list:
        button.draw(img)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break