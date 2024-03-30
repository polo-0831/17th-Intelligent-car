import pyb
#import sys
import sensor, image, time, math
from machine import UART
from pyb import LED
uart = UART(1, baudrate=115200)

LED(4).on()
#green = LED(2)  # 定义一个LED2   绿灯
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) #QVGA:320x240
sensor.set_brightness(1200)
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
clock = time.clock()

# 设置标志位
#Q = 'd'

# 设置地图坐标
map = []

while(True):
    clock.tick()
    #print(sys.version) #3.4.0
    #x = 1
    #print(x)
    #print("{:0>2}".format(x))
    img = sensor.snapshot().lens_corr(1.8)

#绿灯闪烁证明程序运行中----------------------------------------------------------------------
    #green.toggle()

    #if(uart.any()): # 返回等待的字节数量
        #uart_str = uart.readline().strip()
        #uart.write(uart_str)    # 将读取到的串口数据发回
        #if uart_str == b'd':  # 识别地图（di图的d）
            #Q = 'd'

    #if(Q=='d'):
    for r in img.find_rects(threshold = 50000):             # 在图像中搜索矩形
        map = [0,0]
        # 识别到矩形ROI区域的信息
        xr = r.rect()[0]
        yr = r.rect()[1]
        w  = r.rect()[2]
        h  = r.rect()[3]
        if (w >=160 and w <=220 and h >= 120 and h <= 160):

            img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
            img1 = img.copy(r.rect())                           # 提取矩形内ROI区域


            #print_rect = (xr, yr, w, h)
            #print("Rect: xr: %f, yr: %f, w: %f, h: %f" % print_rect)
            for c in img.find_circles(threshold = 2500, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 1, r_max = 5, r_step = 2):
                img.draw_circle(c.x() , c.y() , c.r(), color = (255, 0, 0))

                #k = (xr + w)/700 #虚拟地图和实际地图的比例 （小于1），单位：cm
                #print_point = (c.x(), c.y(), c.r())
                #print("Point: x: %f, y: %f, r: %f" % print_point)

                pi_x = int(((c.x() - xr)/w) * 35)+1  # （（点虚拟距离/地图虚拟边长）* 格子数量 ）+1  根据实测发现大部分坐标少了1，因此强行调整+1
                pi_y = int(((yr + h - c.y())/h) * 25)+1
                map.append(pi_x)
                map.append(pi_y)
            map.append(0)
            map.append(0)
            print(map)
            #for i in range(0, len(map), 2):
                #uart.write("{:0>3}x{:0>3}yZ".format(map[i],map[i+1]))


            uart.write('\r\n')

    #print(clock.fps())
