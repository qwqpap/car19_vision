# 商业转载请联系作者获得授权，非商业转载请注明出处。
# For commercial use, please contact the author for authorization. For non-commercial use, please indicate the source.
# 协议(License)：署名-非商业性使用-相同方式共享 4.0 国际 (CC BY-NC-SA 4.0)
# 作者(Author)：s-ubt-b
# 链接(URL)：https://qwqpap.xyz/2023/11/1088/
# 来源(Source)：天鹅绒房间

#encoding: utf-8

import cv2
import noted
import numpy as np

import serial
import noted
import time

import sys
# from noted import turn_in
from simple_pid import PID

p = PID(Kp=0.23 , Ki=0, Kd=0.01,setpoint=320, output_limits=(-50, 50))

left_start = 0

right_start = 640

up_start = 190

down_start = 250

pressed_pix = 2

speed = 50


def check(x1,x2,y1,y2):
    k=(y2-y1)/(x2-x1)
    if k>0 and k<0.4:
        return 1
    elif k<0 and k>-0.4:
        return -1
    else:
        return False
def is_close(line1, line2, threshold):

    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    #计算两点之间的距离
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # return x2-x1+y2-y1

    # 计算并检查所有可能的端点对之间的距离
    if (distance(x1, y1, x3, y3) < threshold or
        distance(x1, y1, x4, y4) < threshold or
        distance(x2, y2, x3, y3) < threshold or
        distance(x2, y2, x4, y4) < threshold):
        return True

    return False

def turn_in(image):
    # 读取图片
    # image = cv2.imread('WIN_20231126_20_59_29_Pro.jpg')
    # image = cv2.imread('WIN_20231126_21_01_30_Pro.jpg')

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # 应用 Canny 边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 使用 Hough 线变换
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # print(type(lines))
    # 绘制的空白图像
    line_image = np.copy(image) * 0

    # 检查线条
    count=0
    line_check_pos=[]
    line_check_neg=[]
    min_distance=0xffffffff
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if check(x1,x2,y1,y2)==1:
            cv2.line(line_image, (x1, y1), (x2,y2), (255, 0, 0), 3)
            line_check_pos.append(line[0])
        elif check(x1,x2,y1,y2)==-1:
            cv2.line(line_image, (x1, y1), (x2,y2), (255, 0, 0), 3)
            line_check_neg.append(line[0])
    # print(len(line_check_neg)+len(line_check_pos))
    cv2.imshow('Result', line_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for pos in line_check_pos:
        for neg in line_check_neg:
            if is_close(pos,neg,8.6):
                count+=1
    return count>=2





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
        # cnt=1
        while True:

            ret, cap = dev_ca.read()  

            cap = cv2.resize(cap,(640,320))
            if turn_in(cap): #and cnt==1:#检测到三角区域
                err=-50
                bias =math.min(50,abs(err))*0.2
                send_values(ser, 92+err, speed+bias)
                time.sleep(1.05)
                # cnt+=1#第一次
            # elif turn_in(cap) and cnt==2:
            #     err=-50
            #     bias =math.min(50,abs(err))*0.2
            #     send_values(ser, 92+err, speed+bias)
            #     time.sleep(1.05)
            #     cnt+=1#第一次
                
            img = cap

            cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)

            ret,finally_got = cv2.threshold(cap,0,255,cv2.THRESH_OTSU)

            finally_got = ~finally_got

            line, left_line, right_line = find_value_faster(finally_got)

            print(line)

            err =int( p(line))

            print(err)
            
            bias =math.min(50,abs(err))*0.2
            send_values(ser, 92+err, speed+bias)

        cv2.rectangle(finally_got, (left_start, up_start), (right_start, down_start), (255, 0, 255), 3)

        cv2.rectangle(finally_got, (60, up_start), (60, down_start), (255, 0, 255), 3)

        cv2.rectangle(img, (left_line, up_start), (right_line, down_start), (255, 0, 255), 3)

        cv2.line(img,(int(line), int(down_start)), (int(line), int(up_start)),(255,0,255), 3)

        #cv2.rectangle(img, (line, up_start), (line, down_start), (255, 255, 255), 3)

    except KeyError:

        exit()