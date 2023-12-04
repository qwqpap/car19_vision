#!/usr/bin/env python3

'''
以红/蓝锥桶面积之差
作为error输入PID模型
从而控制舵机打角
'''
import json
import rospy
from geometry_msgs.msg import Twist
# import sys, select, termios, tty
import cv2
import numpy as np
import time
from newPID import PID
from stop_line import stop_line
import os
# from camera import *
def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

# PID对象初始化参数
SERVO_kp = 140
SERVO_ki = 0
SERVO_kd = 0
SERVO_imax = 10
# SERVO_kp = 105
# SERVO_ki = 0
# SERVO_kd = 0.2
# SERVO_imax = 10

# MOTOR_kp = 95
# MOTOR_ki = 3
# MOTOR_kd = 0
# MOTOR_imax = 10
timeset = 50

time_stop_start = 11    # 开始执行黄线判断的时间
time_stop_yanshi = 1.1   # 黄线判断成功后延时停止时间
time_stop_this = 40     # 黄线判断成功的时间，40为初始量
stop_line_biao = 0    # 黄线判断成功标志，会被设置为1

time_stop_start_1 = 32    # 开始执行黄线判断的时间
time_stop_yanshi_1 = 0.16   # 黄线判断成功后延时停止时间
time_stop_this_1 = 50     # 黄线判断成功的时间，40为初始量
stop_line_biao_1 = 0    # 黄线判断成功标志，会被设置为1
# PID调用参数
GAIN = 1e-5 # 将PID输出放大或缩小,以适合舵机的打角范围
PID_scale = 1   # 
compensation = 1.1  # 单边颜色缺失增益.因为摄像头比锥桶矮,转直角弯时可能看不见左边红锥桶

# 车模运行参数
set_speed = 1755
set_speed_2 = 1775
control_speed = set_speed    # 500-1499倒车/1500停车/1501-2500前进
turn_mid = 90   # 舵机中值是90
stop_car = True
run = True
# PID对象实例化
SERVO_PID = PID(p = SERVO_kp, i = SERVO_ki, d = SERVO_kd, imax = SERVO_imax)
# MOTOR_PID = PID(p = MOTOR_kp, i = MOTOR_ki, d = MOTOR_kd, imax = MOTOR_imax)


def update(gs, erode, Hmin1, Smin, Vmin, Hmax1, Smax, Vmax, img, Hmin2, Hmax2, img0, size_min):
    # 滤波二值化
    img = cv2.GaussianBlur(img0, (gs, gs), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.erode(img, None, iterations=erode)
    inRange_hsv = cv2.inRange(img, np.array([Hmin1, Smin, Vmin]), np.array([Hmax1, Smax, Vmax]))
    inRange_hsv2 = cv2.inRange(img, np.array([Hmin2, Smin, Vmin]), np.array([Hmax2, Smax, Vmax]))
    img = inRange_hsv + inRange_hsv2
    # 轮廓计算
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    size_all = 0
    target_list = []
    if size_min < 1:
        size_min = 1
    for c in cnts:
        size = cv2.contourArea(c)
        if size < size_min:
            continue
        else:
            target_list.append(c)
            size_all = size_all + size
    return img, size_all, target_list


def detect(img0):
    global gs, erode, Hmin, Smin, Vmin, Hmax, Smax, Vmax, img, Hmin2, Hmax2, size_min
    global gs, erode, Hmin_r, Smin_r, Vmin_r, Hmax_r, Smax_r, Vmax_r, img_r, Hmin2_r, Hmax2_r
    red_dic = read_config('red.json')


    gs = 0
    erode = 2

    size_min = 900
    

    # red  = Color('RED' , 0  , 5 , 158, 179, 150, 255, 50, 250)    
    img = img0.copy()

    # 分别计算蓝/红锥桶面积
    img_b, size_all_b, target_list_b = update(gs, erode, Hmin1, Smin, Vmin, Hmax1, Smax, Vmax, img, Hmin2, Hmax2, img0, size_min)
    img_r, size_all_r, target_list_r = update(gs, erode, Hmin1_r, Smin_r, Vmin_r, Hmax1_r, Smax_r, Vmax_r, img, Hmin2_r, Hmax2_r, img0, size_min)
    # print('size_all_b = '+str(size_all_b))
    # print('size_all_r = '+str(size_all_r))

    #两颜色面积差
    size_difference = size_all_r - size_all_b

    # 若红色面积不足,说明遇到直角弯
    # 直角弯处蓝色锥桶距离较远,故将size_difference适当放大
    if size_all_r <= 1000 or size_all_b <= 1000 : 
        size_difference *= compensation

    print('size_difference = '+str(size_difference))

    if size_all_r <= 1000 and size_all_b <= 1000 :
        return size_difference, True
    else :
        return size_difference, False, size_all_r, size_all_b


if __name__ == "__main__":
    red_dic = read_config('red.json')
    blue_dic = read_config('blue.json')
    ##从配置文件读取HSV参数
    Hmin1_r = red_dic["Hmin1"]
    Hmax1_r = red_dic["Hmax1"]
    Hmin2_r = red_dic["Hmin2"]
    Hmax2_r = red_dic["Hmax2"]
    Smin_r = red_dic["Smin"]
    Smax_r = red_dic["Smax"]
    Vmin_r = red_dic["Vmin"]
    Vmax_r = red_dic["Vmax"]

    Hmin1 = blue_dic["Hmin1"]
    Hmax1 = blue_dic["Hmax1"]
    Hmin2 = blue_dic["Hmin2"]
    Hmax2 = blue_dic["Hmax2"]
    Smin = blue_dic["Smin"]
    Smax = blue_dic["Smax"]
    Vmin = blue_dic["Vmin"]
    Vmax = blue_dic["Vmax"]



    #声明twist节点
    rospy.init_node('racecar_teleop')
    pub = rospy.Publisher('~/car/cmd_vel', Twist, queue_size=5)
    twist = Twist()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    control_turn = turn_mid
    twist.linear.x = 1500
    twist.linear.y = 0
    twist.linear.z = 0
    
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = 90
    pub.publish(twist)
    print("输入y并回车启动:")
    a = input()
    if a=="y":
        pass
    else:
        exit()
    try:
        a = 0
        time_start = time.time()
        while(True):            

            ret, img0 = cap.read()
            size_difference, stop_car, size_all_r, size_all_b = detect(img0)
            time_end = time.time()  # 记录结束时间
            time_sum = time_end - time_start
            print(time_sum)

            # 判断红路灯黄线
            if time_sum >  time_stop_start and time_sum < time_stop_start +15 and stop_line_biao == 0:
                print("------------------")
                if stop_line(img0):
                    print("=============")
                    time_stop_this =time_sum
                    stop_line_biao = 1
                    
            # 判断停车黄线
            if time_sum >  time_stop_start_1 and time_sum < time_stop_start_1 +15 and stop_line_biao_1 == 0:
                print("------------------")
                if stop_line(img0):
                    print("=============")
                    time_stop_this_1 = time_sum
                    stop_line_biao_1 = 1                    
            
            # 红路灯停车
            if stop_line_biao == 1 and time_sum > time_stop_this + time_stop_yanshi and time_sum < time_stop_this + time_stop_yanshi+3:
                i = 1500
                while i:
                    twist.linear.x = 1000
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 90
                    pub.publish(twist)
                    # print(i)
                    i-=1
                    
                os.system(f"gnome-terminal -e 'bash -c \"cd ..; cd ..; cd ..;cd ..; cd workshop/src/autopilot/scripts; python3 slam2.py; exec bash\"'")
                # exit()    
                time.sleep(2.8)
                time_end = time.time()  # 记录结束时间
                time_sum = time_end - time_start
                os.system(f"gnome-terminal -e 'bash -c \"python3 nav.py; exec bash\"'")
                 
                set_speed = set_speed_2
            # 停车    
            if stop_line_biao_1 == 1 and time_sum > time_stop_this_1 + time_stop_yanshi_1 and time_sum < time_stop_this_1 + time_stop_yanshi_1+3:
                i = 1500
                while i:
                    twist.linear.x = 1000
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 90
                    pub.publish(twist)
                    # print(i)
                    i-=1
                os.system(f"gnome-terminal -e 'bash -c \"roslaunch racecar launch.launch; exec bash\"'")                
                exit()
                                
            if time_sum > timeset:
                i = 2000
                while i:
                    twist.linear.x = 1000
                    twist.linear.y = 0
                    twist.linear.z = 0
                    twist.angular.x = 0
                    twist.angular.y = 0
                    twist.angular.z = 90
                    pub.publish(twist)
                    i-=1
                os.system(f"gnome-terminal -e 'bash -c \"roslaunch racecar launch.launch; exec bash\"'")
                print("over")
                exit()                                
             #计算并上传结果
            control_turn = turn_mid - SERVO_PID.get_pid(size_difference, PID_scale) * GAIN
            print('PID: '+str(SERVO_PID.get_pid(size_difference, PID_scale)* GAIN))
            print('TURN: '+str(control_turn))

            #打角限幅
            if control_turn >= 140 :
                control_turn = 140
            if control_turn <= 40  :
                control_turn = 40
            
            #判断是否需要停车
            if stop_car :
                control_speed = 1500
            else :
                control_speed = set_speed
            
            #上传结果
            if control_turn >=80 and control_turn<=100:
                twist.linear.x = control_speed
            else :
                twist.linear.x = control_speed-40
            # twist.linear.x = control_speed
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = control_turn
            pub.publish(twist)
            print('control_speed='+str(control_speed))
            print('control_turn='+str(control_turn))


    except:
        twist = Twist()
        twist.linear.x = 1500; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn_mid
        pub.publish(twist)
    finally:
        twist = Twist()
        twist.linear.x = 1500; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turn_mid
        pub.publish(twist)
