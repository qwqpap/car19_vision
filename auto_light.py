import cv2
import numpy as np

def adjust_brightness(image, alpha, beta):
    # alpha 控制对比度，beta 控制亮度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算灰度图的平均像素值
    average_brightness = np.mean(gray)
    deta = beta - average_brightness
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=deta)
    return adjusted

# 读取图像
image = cv2.imread('img/sun.jpg')

# 设置亮度调整参数
alpha = 0.5  # 对比度，1 表示原始图像对比度不变
beta = 120  # 绝对亮度值

# 调整亮度
adjusted_image = adjust_brightness(image, alpha, beta)

# 显示原始图像和调整后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Adjusted Image', adjusted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
