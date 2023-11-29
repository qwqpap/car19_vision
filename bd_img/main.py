import cv2
import numpy as np
from numba import jit
import serial
import time
import sys

left_start = 20
right_start = 620
up_start = 220
down_start = 240
pressed_pix = 15
@jit
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

def init_send():
    ser = serial.Serial('COM4', 115200, timeout=1)
    return ser

def send_values(ser, servo_value, motor_value):
    # 向串口发送舵机值和电机值
    time.sleep(0.1)
    ser.write(bytes([servo_value, motor_value]))
    while ser.in_waiting:
        arduino_feedback = ser.readline().decode()
        print("Arduino:", arduino_feedback)

if __name__ == "__main__":
    kp = 1
    try:
        ser = init_send()
        cap = cv2.imread("imgs/WIN_20231126_21_01_32_Pro (2).jpg")
        "change here to videos"
        cap = cv2.resize(cap,(640,320))
        img = cap
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        ret,finally_got = cv2.threshold(cap,0,255,cv2.THRESH_OTSU)
        finally_got = ~finally_got
        line, left_line, right_line = find_value(finally_got)
        send_values(ser, 90+(kp*(line-(left_line+right_line)/2)), 50)
        print(line)
        cv2.rectangle(finally_got, (left_start, up_start), (right_start, down_start), (255, 0, 255), 3)
        cv2.rectangle(finally_got, (60, up_start), (60, down_start), (255, 0, 255), 3)
        cv2.rectangle(img, (left_line, up_start), (right_line, down_start), (255, 0, 255), 3)
        cv2.line(img,(int(line), int(down_start)), (int(line), int(up_start)),(255,0,255), 3)
        #cv2.rectangle(img, (line, up_start), (line, down_start), (255, 255, 255), 3)

        cv2.imshow("qwq",img)
        cv2.imshow("pap",finally_got)
        if cv2.waitKey() != "q":
            cv2.destroyAllWindows()

    except:
        cv2.destroyAllWindows()
