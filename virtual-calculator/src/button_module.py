import cv2

class Button():
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (213, 213, 213), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0]+32, self.pos[1]+70), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (50, 50, 50), 2)

    def check_clicked(self, x, y, img):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (150, 100, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 32, self.pos[1] + 70), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (50, 50, 50), 2)
            return True
        return False