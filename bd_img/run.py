import serial
import time
import sys

# 设置串口参数
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

if __name__ == '__main__':
    # 初始化串口
    ser = init_send()
    try:
        while True:
            for i in range(60, 120, 1):
                send_values(ser, i, 50)
                time.sleep(0.1)
            for i in range(120, 60, -1):
                send_values(ser, i, 50)
                time.sleep(0.1)
    except KeyboardInterrupt:
        # 在用户按下 Ctrl+C 时，关闭串口并退出程序
        ser.close()
        sys.exit()
