import cv2
import hand_tracker_module as htm
import button_module as btn

cap = cv2.VideoCapture(1)
cap.set(3, 1280) #width
cap.set(4, 720) #height

detector = htm.HandDetector(detectionCon=0.8)
delay_counter = 0

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

    fingers_up_list = detector.fingers_up()
    if lmList and fingers_up_list[1] and fingers_up_list[2]:
        length, img, info = detector.find_distance(8, 12, img)
        x, y = info[4], info[5]
        if length < 55 and not delay_counter:
            for button in button_list:
                if button.check_clicked(x, y, img):
                    value = button.value
                    print(value)
                    delay_counter = 1

    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break