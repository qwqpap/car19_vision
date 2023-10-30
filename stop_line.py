import cv2
import numpy as np
def stop_line(img):
    down_width = 640
    down_height = 320

    down_points = (down_width, down_height)

    small_img = cv2.resize(img, down_points, interpolation=cv2.INTER_LINEAR)

    hsv = cv2.cvtColor(small_img, cv2.COLOR_BGR2HSV)

    yellow = cv2.inRange(hsv, np.array([100, 130, 50]), np.array([128, 255, 240]))

    all = (yellow.sum())/255

    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    trage_pix = 50

    if all >= trage_pix and cnts >=2:
        return True
    else:
        return False
