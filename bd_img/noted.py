import cv2
import math
import numpy as np
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def update(self, error, dt):
        # 计算积分项
        self.integral += error * dt
        # 计算微分项
        derivative = (error - self.previous_error) / dt
        # 记录当前误差，用于下一次微分计算
        self.previous_error = error
        # 计算PID输出
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        return output


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
    x_start = 0
    y_start = 50
    x_end = 640
    y_end = 320

    # 裁剪图像
    image = image[y_start:y_end, x_start:x_end]
    # 转换为灰度图像
    image = cv2.convertScaleAbs(image, alpha=1.0, beta=20)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # 应用 Canny 边缘检测
    
    edges = cv2.Canny(gray, 80, 220, apertureSize=3)
    
    # 使用 Hough 线变换
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=150, maxLineGap=60)

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
    print(len(line_check_neg)+len(line_check_pos))
    line_image = cv2.addWeighted(image, 0.8, line_image, 3, 0)
    cv2.imshow('Result', line_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for pos in line_check_pos:
        for neg in line_check_neg:
            if is_close(pos,neg,55):
                count+=1
    print(count)
    return count>=1
# image = cv2.imread('C:/Users/fall/Pictures/Camera Roll/WIN_20231126_20_57_48_Pro.jpg.jpg')
image = cv2.imread('WIN_20231126_20_59_29_Pro.jpg')
image = cv2.resize(image,(640,320))
print(turn_in(image))
# print(count)

def  turn_out():
    pass
# 显示图像

# import cv2
# import numpy as np

# class PIDController:
#     def __init__(self, kp, ki, kd):
#         self.kp = kp
#         self.ki = ki
#         self.kd = kd
#         self.previous_error = 0
#         self.integral = 0

#     def update(self, error, dt):
#         # 计算积分项
#         self.integral += error * dt
#         # 计算微分项
#         derivative = (error - self.previous_error) / dt
#         # 记录当前误差，用于下一次微分计算
#         self.previous_error = error
#         # 计算PID输出
#         output = self.kp * error + self.ki * self.integral + self.kd * derivative
#         return output

# # 设置PID参数
# def detect_lane(image):
#     # 转换到灰度图像
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # 应用高斯模糊
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     # Canny 边缘检测
#     edges = cv2.Canny(blur, 100, 170)
    
#     # 霍夫变换检测直线
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, minLineLength=50, maxLineGap=10)
    
#     return lines
# pid = PIDController(kp=0.1, ki=0.01, kd=0.05)

# def get_steering_angle(lines, image_width):
#     line_image = np.copy(image) * 0
#     if lines is None:
#         return 0  # 如果没有检测到线条，返回0表示直行

#     # 初始化左右线条的坐标点
#     left_line_points = []
#     right_line_points = []

#     # 遍历所有检测到的线条，分为左右两组
#     for line in lines:
#         for x1, y1, x2, y2 in line:
#             slope = (y2 - y1) / (x2 - x1)  # 计算斜率
#             if slope < 0 :  # 斜率小于0的为左边的线
#                 left_line_points.append((x1, y1))
#                 left_line_points.append((x2, y2))
#                 cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)

#             elif slope >0:  # 斜率大于0的为右边的线
#                 right_line_points.append((x1, y1))
#                 right_line_points.append((x2, y2))
#                 cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
#     # for r in right_line:
#     #     for l in left_line:
#     #         if 
#     cv2.imshow('Result', line_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     # 计算每边线条的平均点
#     left_avg = np.mean(left_line_points, axis=0) if left_line_points else None
#     right_avg = np.mean(right_line_points, axis=0) if right_line_points else None

#     # 找到最底部的中心点
#     center_point_x = (left_avg[0] + right_avg[0]) / 2 if left_avg is not None and right_avg is not None else image_width / 2

#     # 计算中心点与图像中心的偏差
#     center_offset = center_point_x - (image_width / 2)

#     # 使用PID控制器更新控制信号
#     steering_angle = pid.update(center_offset, dt=1)  # 假设每次调用间隔1秒
#     return steering_angle

# # 使用上述函数
# image = cv2.imread('WIN_20231126_20_58_32_Pro.jpg')
# lines = detect_lane(image)
# steering_angle = get_steering_angle(lines, image.shape[1])
# print(steering_angle)



# combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)


