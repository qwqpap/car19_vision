import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
image = cv2.imread('cross_img/30.jpg')
image = image[280:380, 0:640]
# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用自适应阈值进行二值化
# 高斯卷积核
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 111, -7)

# 进行形态学操作以去除噪声并突出斑马线
kernel = np.ones((5,5), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

sobelx = edges = cv2.Canny(image=morph, threshold1=100, threshold2=200)
x_pixel_counts = np.sum(sobelx, axis=0)
arx = range(len(x_pixel_counts))

print(x_pixel_counts)


plt.figure()

# 绘制折线图
plt.plot(arx,x_pixel_counts, label='pix_number')
zero_intervals = []
start = None
for i, count in enumerate(x_pixel_counts):
    if count == 0 and start is None:
        start = i
    elif count != 0 and start is not None:
        end = i - 1
        if end - start + 1 > 10:  # 假设长度大于10的区间才算有效
            zero_intervals.append((start, end))
        start = None

# 打印找到的区间
print("Zero intervals:", zero_intervals)

# 可视化结果
plt.plot(x_pixel_counts)
for (start, end) in zero_intervals:
    plt.axvspan(start, end, color='pink', alpha=1)
plt.xlabel('x')
plt.ylabel('Pixel Count')
plt.show()

cv2.imshow('Detected Zebra Crossings', sobelx)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 检查是否存在4个这样的区间
if len(zero_intervals) >= 4:
    print("Detected Zebra Crossing")
else:
    print("No Zebra Crossing Detected")


def if_cross(img) -> bool:

    img = img[280:380, 0:640]
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用自适应阈值进行二值化
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 81, -7)

    # 进行形态学操作以去除噪声并突出斑马线
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    sobelx = edges = cv2.Canny(image=morph, threshold1=100, threshold2=200)
    x_pixel_counts = np.sum(sobelx, axis=0)
    arx = range(len(x_pixel_counts))

    zero_intervals = []
    start = None
    for i, count in enumerate(x_pixel_counts):
        if count == 0 and start is None:
            start = i
        elif count != 0 and start is not None:
            end = i - 1
            if end - start + 1 > 10:  # 假设长度大于10的区间才算有效
                zero_intervals.append((start, end))
            start = None



    # 检查是否存在4个这样的区间
    if len(zero_intervals) >= 4:

        return True
    else:
        return False



