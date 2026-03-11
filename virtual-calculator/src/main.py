import cv2
import hand_tracker_module as htm
import button_module as btn

cap = cv2.VideoCapture(1)
cap.set(3, 1280) # width
cap.set(4,720) # height
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

button_list = []
button_list_values = [['7', '8', '9', '*'],
                      ['4', '5', '6', '-'],
                      ['1', '2', '3', '+'],
                      ['0', '/', '.', '=']]

for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        button_list.append(btn.Button((xpos, ypos), 100, 100, button_list_values[y][x]))
button_list.append(btn.Button((750, 50), 50, 100, 'c'))
button_list.append(btn.Button((700, 50), 50, 100, 'b'))

current_equation = ''

delay_counter = 0

def is_valid_operation(current_equation, value):
    operations = ('+', '-', '/', '*')
    if value == '.' and current_equation[-1:] == '.':
        return False
    if value == '0' and current_equation[-1:] == '/':
        return False
    if not value in operations:
        return True
    if not current_equation and value in ('/', '*'):
        return False
    if not (current_equation[-1:] in operations):
        return True
    if value == '*' :
        if current_equation[-2:] == '**' or current_equation[-1:] in ('+', '-', '/'):
            return False
        return True
    return False


while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList = detector.find_position(img)

    for button in button_list:
        button.draw(img)

    cv2.rectangle(img, (800, 50), (800 + 400, 50 + 100),
                  (213, 213, 213), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 50 + 100),
                  (50, 50, 50), 3)

    cv2.putText(img, current_equation, (810, 120), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (50, 50, 50), 3)

    fingers_up_list = detector.fingers_up()
    if lmList and fingers_up_list[1] and fingers_up_list[2]:
        length, img, info = detector.find_distance(8, 12, img)
        x, y = info[4], info[5]
        if length < 55 and not delay_counter:
            for button in button_list:
                if button.check_clicked(x, y, img):
                    value = button.value
                    if value == '=' :
                        current_equation = str(eval(current_equation))
                    elif value == 'c' :
                        current_equation = ''
                    elif value == 'b':
                        current_equation = current_equation[:-1]
                    else:
                        if is_valid_operation(current_equation, value):
                            current_equation += value
                    delay_counter = 1

    if delay_counter != 0:
        delay_counter += 1
        if delay_counter > 10:
            delay_counter = 0

    cv2.imshow("Virtual Calc", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break