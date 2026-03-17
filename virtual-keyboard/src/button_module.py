import cv2

class Button():
    def __init__(self, pos, value, width=70, height=70):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (213, 213, 213), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (50, 50, 50), 2)
        cv2.putText(img, self.value.capitalize(), (int(self.pos[0] + self.width / 3.9), int(self.pos[1]+ self.height / 1.4)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (50, 50, 50), 2)

    def check_hover(self, x, y, img):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (100, 100, 100), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 2)
            cv2.putText(img, self.value.capitalize(), (int(self.pos[0] + self.width / 3.9), int(self.pos[1] + self.height / 1.4)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (50, 50, 50), 2)
            return True
        return False

    def check_clicked(self, x, y, img):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (0, 200, 0), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 2)
            cv2.putText(img, self.value.capitalize(), (int(self.pos[0] + self.width / 3.9), int(self.pos[1] + self.height / 1.4)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (50, 50, 50), 2)
            return True
        return False