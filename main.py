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

        start_pix = 80
        end_pix = 250

        detected_img = small_img[start_pix:end_pix, 0:640]

        hsv = cv2.cvtColor(detected_img, cv2.COLOR_BGR2HSV)

        blue_shv = [[100, 128], [130, 255], [50, 240]]

        red_hsv = [[0, 24], [149, 255], [85, 240]]

        blue_inrange = cv2.inRange(hsv, np.array([100, 130, 50]), np.array([128, 255, 240]))
        red_inrange = cv2.inRange(hsv, np.array([0, 149, 85]), np.array([24, 255, 240]))
        cv2.imshow("qwq", blue_inrange)
        cv2.imshow("pap", red_inrange)
        blue_inrange = blue_inrange.astype(np.int32)
        red_inrange = red_inrange.astype(np.int32)
        different = np.sum(red_inrange)
        print(different)
        different -= np.sum(blue_inrange)
        print(different)

        if cv2.waitKey() != "q":

            cv2.destroyAllWindows()

        print(different)
        return different


if __name__ == "__main__":
    img = cv2.imread("img/0.jpg")
    find = FindMiddleLine(img)
    find.find_line()