
#encoding: utf-8

import cv2

import numpy as np

import serial

import time

import sys

from simple_pid import PID

p = PID(Kp=0.23, Ki=0, Kd=0.01, setpoint=320, output_limits=(-50, 50))

left_start = 0

right_start = 640

up_start = 190

down_start = 250

pressed_pix = 2

speed = 50

def find_value(img11):

    # 计算灰度直方图

    global left_start, right_start, up_start, down_start

    finally_list = []

    mid_num = int((right_start + left_start) / 2)

    for i in range(left_start, right_start):

        # error_now = i - mid_num

        n = 0

        for j in range(up_start, down_start):

            if img11[j, i] >= 128:

                n = n + 1

            else:

                pass

        finally_list.append(n)

    #print(finally_list)

    '''

    x = np.array(range(0,len(finally_list)))

    y = np.array(finally_list)

    plt.bar(x,y,0.8)

    plt.show()

    '''

    left_line = left_start

    right_line = right_start

    # fina_error = int(fina_error/sigema + mid_num)

    for i in range(mid_num, right_start-left_start):

        if finally_list[i] >= pressed_pix:

            right_line = i + left_start

            #print(i)

            break

        else:

            pass

    for i in range(mid_num, 0, -1):

        if finally_list[i] >= 1+pressed_pix:

            left_line = i + left_start

            #print(i)

            break

        else:

            pass

    line = (left_line + right_line) / 2

    return line, left_line, right_line

def find_value_faster(img11):

        global left_start, right_start, up_start, down_start

        # 提取需要处理的部分图像

        img_part = img11[up_start:down_start, left_start:right_start]

        # 将图像转换为布尔类型的数组，表示像素值是否大于等于128

        bool_img = img_part >= 128

        # 沿水平方向对布尔数组进行求和，得到每列像素值大于等于128的数量

        finally_list = np.sum(bool_img, axis=0)

        pressed_pix = 2  # 请替换为合适的值

        # 计算中间数值

        mid_num = int((right_start + left_start) / 2)

        i = 320

        while finally_list[i] <= pressed_pix and 1<i<639:

            i = i + 1

        right_line = i

        i =320

        while finally_list[i] <= pressed_pix and 1<i<639:

            i = i - 1

        left_line = i

        # 查找右边界

        pressed_pix = 10  # 请替换为合适的值

        line = (left_line + right_line) / 2

        return line, left_line, right_line

def init_send():

    ser = serial.Serial('/dev/arduino', 115200, timeout=1)

    return ser

def send_values(ser, servo_value, motor_value):

    # 向串口发送舵机值和电机值

    time.sleep(0.05)

    ser.write(bytes([servo_value, motor_value]))

    while ser.in_waiting:

        arduino_feedback = ser.readline().decode()

        # print("Arduino:", arduino_feedback)

error_last = 0

error_this = 0

if __name__ == "__main__":

    kp = 0.4

    try:

        #ser = init_send()

        dev_ca = cv2.VideoCapture(0)

        ser = serial.Serial('/dev/arduino', 115200, timeout=1)

        while True:

            ret, cap = dev_ca.read()  

            cap = cv2.resize(cap,(640,320))

            img = cap

            cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

            ret,finally_got = cv2.threshold(cap,0,255,cv2.THRESH_OTSU)

            finally_got = ~finally_got

            line, left_line, right_line = find_value_faster(finally_got)

            print(line)

            err =int( p(line))

            print(err)

            send_values(ser, 92+err, speed)

        cv2.rectangle(finally_got, (left_start, up_start), (right_start, down_start), (255, 0, 255), 3)

        cv2.rectangle(finally_got, (60, up_start), (60, down_start), (255, 0, 255), 3)

        cv2.rectangle(img, (left_line, up_start), (right_line, down_start), (255, 0, 255), 3)

        cv2.line(img,(int(line), int(down_start)), (int(line), int(up_start)),(255,0,255), 3)

        #cv2.rectangle(img, (line, up_start), (line, down_start), (255, 255, 255), 3)

    except KeyError:

        exit()