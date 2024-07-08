# -*- coding: utf-8 -*-
import cv2
import numpy as np


class LineFinder:
    def __init__(self):
        self.in_doing_img = None
        self.image = None
        self.image_size = (640, 480)
        self.cut_range = [(0, 240), (640, 480)]
        self.image_path = 'photo/11.jpg'
        self.Flag = "Not start"
        self.capture = cv2.VideoCapture(0)

    def read_image(self):
        self.image = cv2.imread(self.image_path, 0)
        self.Flag = "Now Process"

    def read_cap(self):
        ret, frame = self.capture.read()
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # cv2.imshow("show_time", img)
        img = cv2.resize(img, (640, 480))
        return img

    # 预处理裁切,模糊与大津法
    def img_pre_deal(self):
        self.image = cv2.resize(self.image, self.image_size)
        cut_image = self.image[self.cut_range[0][1]:self.cut_range[1][1], self.cut_range[0][0]:self.cut_range[1][0]]
        gauss_img = cv2.GaussianBlur(cut_image, (25, 25), sigmaX=0, sigmaY=0)
        edge_img = cv2.adaptiveThreshold(gauss_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 81, -7)
        kernel = np.ones((5, 5), dtype=np.uint8)
        edge_img = cv2.erode(edge_img, kernel, 1)
        self.in_doing_img = edge_img
        # cv2.imshow("show_time", edge_img)
        # cv2.waitKey(0)

    def line_find(self, mode="normal"):
        if self.in_doing_img is None:
            return False
        else:
            pass
        left_start = 0
        right_start = 640
        up_start = 80
        down_start = 100  # 提取需要处理的部分图像
        img_part = self.in_doing_img[up_start:down_start, left_start:right_start]  # 将图像转换为布尔类型的数组，表示像素值是否大于等于128
        bool_img = img_part >= 128  # 沿水平方向对布尔数组进行求和，得到每列像素值大于等于128的数量
        finally_list = np.sum(bool_img, axis=0)
        pressed_pix = 3  # 请替换为合适的值
        # 计算中间数值
        mid_num = int((right_start + left_start) / 2)
        i = 320
        while finally_list[i] <= pressed_pix and 1 < i < 639:
            i = i + 1
        right_line = i
        i = 320
        while finally_list[i] <= pressed_pix and 1 < i < 639:
            i = i - 1
        left_line = i  # 查找右边界
        pressed_pix = 10  # 请替换为合适的值
        mid_line = (left_line + right_line) / 2

        # test used
        if mode == "test":
            draw_0 = cv2.rectangle(self.in_doing_img, (left_line, up_start), (right_line, down_start), (255, 0, 0), 2)
            cv2.imshow("test", draw_0)
            cv2.waitKey(0)
        else:
            pass

        if left_line <= 1 and right_line >= 639:
            flag = "end"
        elif left_line <= 1:
            flag = "left"
        elif right_line >= 639:
            flag = "right"
        else:
            flag = "normal"

        return mid_line, flag

    def process(self, mode="cam"):
        """

        :param mode: input : "cam" or "test"
        :return: int : line, flag : "normal", "end", "left", "right"
        """
        flags = "normal"
        if mode == 'cam':
            this_frame = self.read_cap()
            self.image = this_frame
            self.img_pre_deal()
            loc, flags = self.line_find()
            loc = loc / self.image_size[0]
            return loc, flags
        elif mode == "test":
            self.read_image()
            self.img_pre_deal()
            loc, flags = self.line_find("test")
            return 0, 0
if __name__ == "__main__":
    line = LineFinder()
    while True:
        line_mid, flag = line.process("cam")
        # cv2.imshow("img",line.in_doing_img)
        # cv2.waitKey(0)
        print(line_mid)
        print(flag)
