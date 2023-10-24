import cv2
import numpy as np
import time
import numba

class FindMiddleLine:
    def __init__(self, raw_img):
        self.raw_img = raw_img

    def find_line(self):
        img = self.raw_img

        down_width = 640
        down_height = 320

        down_points = (down_width, down_height)

        small_img = cv2.resize(img, down_points, interpolation=cv2.INTER_LINEAR)

        start_pix = 130
        end_pix = 150

        detected_img = small_img[start_pix:end_pix, 0:640]

        hsv = cv2.cvtColor(detected_img, cv2.COLOR_BGR2HSV)

        blue_shv = [[100, 128], [130, 255], [50, 240]]

        red_hsv = [[0, 24], [149, 255], [85, 240]]

        blue_inrange = cv2.inRange(hsv, np.array([100, 130, 50]), np.array([128, 255, 240]))
        red_inrange = cv2.inRange(hsv, np.array([0, 149, 85]), np.array([24, 255, 240]))

        cv2.imshow("qwq", blue_inrange)
        cv2.imshow("pap", red_inrange)

        blue_left = 320
        blue_right = 320

        for i in range(640):
            # error_now = i - mid_num
            n = 0
            for j in range(20):
                if blue_inrange[j, i] >= 200:
                    n = n + 1
                else:
                    pass

            if n >= 10:
                blue_left = i
                break

        for i in range(639, 0, -1):

            # error_now = i - mid_num
            n = 0
            for j in range(20):
                if blue_inrange[j, i] >= 200:
                    n = n + 1
                else:
                    pass
            if n >= 10:
                blue_right = i
                break

        print(blue_right)
        print(blue_left)

        red_left = 0
        red_right = 0

        for i in range(640):
            # error_now = i - mid_num
            n = 0
            for j in range(20):
                if red_inrange[j, i] >= 200:
                    n = n + 1
                else:
                    pass

            if n >= 10:
                red_left = i
                break

        for i in range(639, 0, -1):

            # error_now = i - mid_num
            n = 0
            for j in range(20):
                if red_inrange[j, i] >= 200:
                    n = n + 1
                else:
                    pass
            if n >= 10:
                red_right = i
                break

        print(red_right)
        print(red_left)

        cv2.imshow("red",red_inrange)
        cv2.imshow("blue",blue_inrange)

        if cv2.waitKey(1) != "q":
            time.sleep(10)
            cv2.destroyAllWindows()

        mid = (blue_left + red_right)/640
        print(mid)
        return mid
if __name__ == "__main__":
    #img = cv2.imread("img/16.jpg")
    video = cv2.VideoCapture(0)
    ret,img = video.read()
    find = FindMiddleLine(img)
    find.find_line()