import cv2
import numpy as np
import json

def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config
yellow_dic = read_config('yellow.json')
Hmin = yellow_dic["Hmin1"]
Hmax= yellow_dic["Hmax1"]
Smin= yellow_dic["Smin"]
Smax = yellow_dic["Smax"]
Vmin =  yellow_dic["Vmin"]
Vmax = yellow_dic["Vmax"]
def stop_line(img):
    global  Hmin, Smin, Vmin, Hmax, Smax, Vmax, Hmin2, Hmax2
    down_width = 640
    down_height = 320

    down_points = (down_width, down_height)

    small_img = cv2.resize(img, down_points, interpolation=cv2.INTER_LINEAR)

    start_pix = 200
    end_pix = 250

    small_img = small_img[start_pix:end_pix, 0:640]

    hsv = cv2.cvtColor(small_img, cv2.COLOR_BGR2HSV)


    yellow = cv2.inRange(hsv, np.array([Hmin, Smin, Vmin]), np.array([Hmax, Smax, Vmax]))

    all_pix = (yellow.sum()) / 255

    target_pix = 50

    if all_pix >= target_pix:
        return True
    else:
        return False


if __name__ == "__main__":
    img = cv2.imread("stop_photo/4.jpg")
    fina = stop_line(img)
    print(fina)
