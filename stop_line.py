import cv2
import numpy as np


def stop_line(img):
    down_width = 640
    down_height = 320

    down_points = (down_width, down_height)

    small_img = cv2.resize(img, down_points, interpolation=cv2.INTER_LINEAR)

    start_pix = 200

    end_pix = 250

    small_img = small_img[start_pix:end_pix, 0:640]

    hsv = cv2.cvtColor(small_img, cv2.COLOR_BGR2HSV)

    yellow = cv2.inRange(hsv, np.array([100, 130, 50]), np.array([128, 255, 240]))

    all = (yellow.sum()) / 255

    target_pix = 50

    if all >= target_pix:
        return True
    else:
        return False


if __name__ == "__main__":
    img = cv2.imread("stop_photo/4.jpg")
    fina = stop_line(img)
    print(fina)
