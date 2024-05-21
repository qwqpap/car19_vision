import cv2
import numpy as np
import matplotlib.pyplot as plt

trigger_pix = 18000
# 读取图像
image = cv2.imread('cross_img/25.jpg')
image = image[280:380, 0:640]
# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用自适应阈值进行二值化
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,81,-7)

# 进行形态学操作以去除噪声并突出斑马线
kernel = np.ones((5,5), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

sobelx = edges = cv2.Canny(image=morph, threshold1=100, threshold2=200)
y_sum = np.sum(sobelx, axis=0)
arx = range(len(y_sum))


max_tar = np.max(y_sum)
if max_tar >= trigger_pix:
    flag = True

print(y_sum)

cv2.imshow('Detected Zebra Crossings', sobelx)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.figure()

# 绘制折线图
plt.plot(arx,y_sum, label='pix_number')
# 添加标题和标签
plt.title('Pix_det')
plt.xlabel('x')
plt.ylabel('pix_number')

# 显示图例
plt.legend()

# 显示图形
plt.show()