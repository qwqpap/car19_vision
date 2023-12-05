import json  # 用于保存配置到文件
import cv2
import numpy as np
import time

"""

1. R 按下代表保存红色参数
2. T 按下代表读取红色参数
3. B 按下代表保存蓝色参数
4. N 按下代表读取蓝色参数
5. Y 按下代表保存黄色参数
6. U 按下代表读取黄色参数

"""

# 'camera' or 'picture'
mode = 'picture'

if mode == 'camera':
    cap = cv2.VideoCapture(0)


def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def update(x):
    global gs, erode, Hmin, Smin, Vmin, Hmax, Smax, Vmax, img, Hmin2, Hmax2, img0, size_min

    if mode == 'camera':
        ret, img0 = cap.read()
    elif mode == 'picture':
        img0 = cv2.imread('pap.jpg')
    img = img0.copy()

    gs = cv2.getTrackbarPos('gs', 'image')
    erode = cv2.getTrackbarPos('erode', 'image')
    Hmin = cv2.getTrackbarPos('Hmin1', 'image')
    Smin = cv2.getTrackbarPos('Smin', 'image')
    Vmin = cv2.getTrackbarPos('Vmin', 'image')
    Hmax = cv2.getTrackbarPos('Hmax1', 'image')
    Smax = cv2.getTrackbarPos('Smax', 'image')
    Vmax = cv2.getTrackbarPos('Vmax', 'image')
    Hmin2 = cv2.getTrackbarPos('Hmin2', 'image')
    Hmax2 = cv2.getTrackbarPos('Hmax2', 'image')
    size_min = cv2.getTrackbarPos('size_min', 'image')
    # 滤波二值化
    gs_frame = cv2.GaussianBlur(img, (gs, gs), 1)
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    erode_hsv = cv2.erode(hsv, None, iterations=erode)
    inRange_hsv = cv2.inRange(erode_hsv, np.array([Hmin, Smin, Vmin]), np.array([Hmax, Smax, Vmax]))
    inRange_hsv2 = cv2.inRange(erode_hsv, np.array([Hmin2, Smin, Vmin]), np.array([Hmax2, Smax, Vmax]))
    img = inRange_hsv + inRange_hsv2
    # 外接计算
    print(img.sum())
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    target_list = []
    pos = []
    if size_min < 1:
        size_min = 1
    for c in cnts:
        if cv2.contourArea(c) < size_min:
            continue
        else:
            target_list.append(c)
    for cnt in target_list:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img0, (x, y), (x + w, y + h), (0, 255, 0), 2)
        pos.append([int(x + w / 2), y + h / 2])
    #print(pos)

def save_config(filename):
    config = {
        'gs': cv2.getTrackbarPos('gs', 'image'),
        'erode': cv2.getTrackbarPos('erode', 'image'),
        'Hmin1': cv2.getTrackbarPos('Hmin1', 'image'),
        'Hmax1': cv2.getTrackbarPos('Hmax1', 'image'),
        'Hmin2': cv2.getTrackbarPos('Hmin2', 'image'),
        'Hmax2': cv2.getTrackbarPos('Hmax2', 'image'),
        'Smin': cv2.getTrackbarPos('Smin', 'image'),
        'Smax': cv2.getTrackbarPos('Smax', 'image'),
        'Vmin': cv2.getTrackbarPos('Vmin', 'image'),
        'Vmax': cv2.getTrackbarPos('Vmax', 'image'),
        'size_min': cv2.getTrackbarPos('size_min', 'image')
    }

    with open(filename, 'w') as f:
        json.dump(config, f)

    print(f'Parameters saved to {filename}')

def img_test():
    sleep = 0.1
    gs = 0
    erode = 0
    Hmin1 = 100
    Hmax1 = 125
    Hmin2 = 179
    Hmax2 = 0
    Smin = 130
    Smax = 255
    Vmin = 50
    Vmax = 240
    size_min = 1000

    # 创建窗口
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('gs', 'image', 0, 8, update)
    cv2.createTrackbar('erode', 'image', 0, 8, update)
    cv2.createTrackbar('Hmin1', 'image', 0, 179, update)
    cv2.createTrackbar('Hmax1', 'image', 0, 179, update)
    cv2.createTrackbar('Hmin2', 'image', 0, 179, update)
    cv2.createTrackbar('Hmax2', 'image', 0, 179, update)
    cv2.createTrackbar('Smin', 'image', 0, 255, update)
    cv2.createTrackbar('Smax', 'image', 0, 255, update)
    cv2.createTrackbar('Vmin', 'image', 0, 255, update)
    cv2.createTrackbar('Vmax', 'image', 0, 255, update)
    cv2.createTrackbar('size_min', 'image', 1, 100000, update)
    # 默认值
    cv2.setTrackbarPos('gs', 'image', gs)
    cv2.setTrackbarPos('erode', 'image', erode)
    cv2.setTrackbarPos('Hmin1', 'image', Hmin1)
    cv2.setTrackbarPos('Hmax1', 'image', Hmax1)
    cv2.setTrackbarPos('Hmin2', 'image', Hmin2)
    cv2.setTrackbarPos('Hmax2', 'image', Hmax2)
    cv2.setTrackbarPos('Smin', 'image', Smin)
    cv2.setTrackbarPos('Smax', 'image', Smax)
    cv2.setTrackbarPos('Vmin', 'image', Vmin)
    cv2.setTrackbarPos('Vmax', 'image', Vmax)
    cv2.setTrackbarPos('size_min', 'image', size_min)

    while True:
        try:
            update(1)
        except:
            pass
        cv2.imshow('image', img)
        cv2.imshow('image1', img)
        cv2.imshow('image0', img0)
        key = cv2.waitKey(1)

        # 检查按键事件
        if key == ord('r'):  # 如果按下 'r' 键
            save_config('red.json')
        elif key == ord('b'):  # 如果按下 'b' 键
            save_config('blue.json')
        elif key == ord('y'):  # 如果按下 'h' 键
            save_config('yellow.json')
        elif key == ord('t'):
            red_dic = read_config('red.json')

            cv2.setTrackbarPos('gs', 'image', red_dic["gs"])
            cv2.setTrackbarPos('erode', 'image', red_dic["erode"])
            cv2.setTrackbarPos('Hmin1', 'image', red_dic["Hmin1"])
            cv2.setTrackbarPos('Hmax1', 'image', red_dic["Hmax1"])
            cv2.setTrackbarPos('Hmin2', 'image', red_dic["Hmin2"])
            cv2.setTrackbarPos('Hmax2', 'image', red_dic["Hmax2"])
            cv2.setTrackbarPos('Smin', 'image', red_dic["Smin"])
            cv2.setTrackbarPos('Smax', 'image', red_dic["Smax"])
            cv2.setTrackbarPos('Vmin', 'image', red_dic["Vmin"])
            cv2.setTrackbarPos('Vmax', 'image', red_dic["Vmax"])
            cv2.setTrackbarPos('size_min', 'image', red_dic["size_min"])
        elif key == ord('n'):
            blue_dic = read_config('blue.json')

            cv2.setTrackbarPos('gs', 'image', blue_dic["gs"])
            cv2.setTrackbarPos('erode', 'image', blue_dic["erode"])
            cv2.setTrackbarPos('Hmin1', 'image', blue_dic["Hmin1"])
            cv2.setTrackbarPos('Hmax1', 'image', blue_dic["Hmax1"])
            cv2.setTrackbarPos('Hmin2', 'image', blue_dic["Hmin2"])
            cv2.setTrackbarPos('Hmax2', 'image', blue_dic["Hmax2"])
            cv2.setTrackbarPos('Smin', 'image', blue_dic["Smin"])
            cv2.setTrackbarPos('Smax', 'image', blue_dic["Smax"])
            cv2.setTrackbarPos('Vmin', 'image', blue_dic["Vmin"])
            cv2.setTrackbarPos('Vmax', 'image', blue_dic["Vmax"])
            cv2.setTrackbarPos('size_min', 'image', blue_dic["size_min"])
        elif key == ord('u'):
            yellow_dic = read_config('blue.json')

            cv2.setTrackbarPos('gs', 'image', yellow_dic["gs"])
            cv2.setTrackbarPos('erode', 'image', yellow_dic["erode"])
            cv2.setTrackbarPos('Hmin1', 'image', yellow_dic["Hmin1"])
            cv2.setTrackbarPos('Hmax1', 'image', yellow_dic["Hmax1"])
            cv2.setTrackbarPos('Hmin2', 'image', yellow_dic["Hmin2"])
            cv2.setTrackbarPos('Hmax2', 'image', yellow_dic["Hmax2"])
            cv2.setTrackbarPos('Smin', 'image', yellow_dic["Smin"])
            cv2.setTrackbarPos('Smax', 'image', yellow_dic["Smax"])
            cv2.setTrackbarPos('Vmin', 'image', yellow_dic["Vmin"])
            cv2.setTrackbarPos('Vmax', 'image', yellow_dic["Vmax"])
            cv2.setTrackbarPos('size_min', 'image', yellow_dic["size_min"])
        elif key == 27:  # 如果按下 ESC 键
            break

        time.sleep(0.1)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    img_test()