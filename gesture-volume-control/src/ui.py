import cv2
import numpy as np

def draw_ui(img, vol_percentage, muted=False):
    bar_x = 50
    bar_y = 150
    bar_width= 30
    bar_height = 200

    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)

    fill_height = int(np.interp(vol_percentage, [0, 100], [0, bar_height]))
    fill_start_y = bar_y + (bar_height - fill_height)

    if muted:
        bar_color = (199, 199, 199)
        text_color = (255, 255, 255)
    elif vol_percentage < 5:
        bar_color = (0, 0, 255)
        text_color = (0, 0, 255)
    elif vol_percentage > 95:
        bar_color = (0, 255, 0)
        text_color = (0, 255, 0)
    else:
        bar_color = (77, 77, 77)
        text_color = (255, 255, 255)

    # Volume bar (filled based on the percentage and shows the percentage)

    cv2.rectangle(img, (bar_x, fill_start_y), (bar_x + bar_width, bar_y + bar_height), bar_color, cv2.FILLED)
    cv2.putText(img, f"{int(vol_percentage)}%", (bar_x - 10, bar_y + bar_height + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)


    # Speaker icon (indicates muted/unmuted

    icon_x = bar_x + 2
    icon_y = bar_y - 60

    cv2.rectangle(img, (icon_x, icon_y + 10),
                  (icon_x + 12, icon_y + 25),
                  (255, 255, 255), cv2.FILLED)

    cv2.polylines(img,
                  [np.array([[icon_x + 12, icon_y + 5],
                             [icon_x + 24, icon_y],
                             [icon_x + 24, icon_y + 35],
                             [icon_x + 12, icon_y + 30]])],
                  True,
                  (255, 255, 255),
                  2)

    # Red X if muted
    if muted:
        cv2.line(img, (icon_x - 3, icon_y - 3),
                 (icon_x + 27, icon_y + 33),
                 (0, 0, 255), 2)
        cv2.line(img, (icon_x + 27, icon_y - 3),
                 (icon_x - 3, icon_y + 33),
                 (0, 0, 255), 2)