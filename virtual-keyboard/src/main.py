import cv2
import hand_tracker_module as htm
import button_module as btn

cap = cv2.VideoCapture(1)
cap.set(3, 1280) #width
cap.set(4, 720) #height

detector = htm.HandDetector(detectionCon=0.8)
delay_counter = 0

button_list = []

english_keyboard_value = [['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'bs'],
                          ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
                          ['', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''],
                          ['ctrl', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']]

english_keyboard_alternative = {'`': '~',
                                '1': '!',
                                '2': '@',
                                '3': '#',
                                '4': '$',
                                '5': '%',
                                '6': '^',
                                '7': '&',
                                '8': '*',
                                '9': '(',
                                '0': ')',
                                '-': '_',
                                '=': '+',
                                ';': ':',
                                '\'': '\"',
                                '[': '{',
                                ']': '}',
                                '\\': '|',
                                ',': '<',
                                '.': '>',
                                '/': '?'}

caps_button = btn.FuncButton((80 * 0 + 85, 80 * 2 + 20), 'cap')
shift_button = btn.FuncButton((80 * 11 + 85, 80 * 3 + 20), 'shift', 230)

for y in range(len(english_keyboard_value)):
    for x, value in enumerate(english_keyboard_value[y]):
        if value == '':
            continue
        if value in english_keyboard_alternative.keys():
            alt_value = english_keyboard_alternative[value]
        else :
            alt_value = None
        button_list.append(btn.Button((80 * x + 85, 80 * y + 20), value, alt_value = alt_value))
button_list.append(btn.Button((80 * 12 + 85, 80 * 2 + 20), 'enter', 150))
button_list.append(caps_button)
button_list.append(shift_button)
button_list.append(btn.Button((85, 80 * 4 + 20), 'alt'))
button_list.append(btn.Button((165, 80 * 4 + 20), ' ', 70 * 4 + 30, 70))

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

        if not delay_counter:
            for button in button_list:
                if button.check_hover(x, y, img) and length < 55:
                    if button.check_clicked(x, y, img):
                        value = button.value
                        if caps_button.is_pressed:
                            value = button.value.capitalize()
                        if shift_button.is_pressed:
                            value = button.alt_value
                        print(value)
                        delay_counter = 1

    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break