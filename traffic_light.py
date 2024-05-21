import cv2
import numpy as np



def get_points(img ,hsvmin ,hsv_max ,gs ,erode) -> list:

    img = cv2.GaussianBlur(img, (gs, gs), 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.erode(hsv, None, iterations=erode)
    dst = cv2.inRange(hsv, hsvmin, hsv_max)
    cv2.imshow("qwq",dst)
    cnts = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    cv2.waitKey(0)
    pos = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), 255, 2)
        pos.append([int(x + w / 2), y + h / 2])
    return pos

def crossing_line():
    pass



mode = "pic" # or "videos"



if __name__ == "__main__":
    if mode == "videos":
        cap = cv2.VideoCapture(-1)


        try:

            while True:

                ret, frame = cap.read()
                frame = frame[0:480, 0:640]
                # red

                red_points = get_points(frame, np.array([144, 220, 225]), np.array([179, 255, 255]), 7, 0)

                # green

                green_points = get_points(frame, np.array([46, 90, 179]), np.array([69, 206, 255]), 7, 0)

        except:
            print("cant read the cam")

    else:
        im = cv2.imread("cross_img/11.jpg")
        im = im[0:480, 0:640]
        red_points = get_points(im, np.array([144, 220, 220]), np.array([179, 255, 255]), 7, 0)
        green_points = get_points(im, np.array([71, 119, 145]), np.array([89, 255, 255]), 7, 0)

        print(red_points)
        print(green_points)