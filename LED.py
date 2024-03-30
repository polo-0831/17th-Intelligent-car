import pyb
from pyb import LED #导入LED
from machine import UART

print('Start test LED\r\n') # 通过串口3输出提示信息 C8为TX C9为RX
red = LED(1)    # 定义一个LED1   红灯
green = LED(2)  # 定义一个LED2   绿灯
blue = LED(3)   # 定义一个LED3   蓝灯
white = LED(4)  # 定义一个LED4   照明灯
uart1 = UART(1, baudrate=115200)

Q = 'r'
while(True):

    if(uart1.any()): # 返回等待的字节数量
        uart_str = uart1.readline().strip().decode()
        #print(uart_str)

        #uart_str是byte型变量为b''，用decode方法转换为字符串格式变量
        #uart.write(uart_str)    # 将读取到的串口数据发回
        if uart_str == 'r': # 识别矩形
            #print(uart_str)
            Q = 'r'
        elif uart_str == 'm': # 运行模型识别
            #print(uart_str)
            Q = 'm'

    if Q == 'r':
        red.on()        # 打开红灯
    else:
        red.off()

    if Q == 'm':
        green.on()
    else:
        green.off()







