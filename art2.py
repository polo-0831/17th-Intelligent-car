import pyb
import sensor, image, time, math
from machine import UART
from pyb import LED
#import SEEKFREE_18TFT as tft18
# 初始化串口 波特率设置为115200 TX是B12 RX是B13
uart1 = UART(1, baudrate=115200)

LED(4).on()
green = LED(2)  # 定义一个LED2   绿灯
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.HQVGA) #QQVGA:240x160
sensor.set_brightness(1200)
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
#tft18.tft_init()
clock = time.clock()

# 定义中心坐标数组
center = [0, 0] #160x120内的像素坐标
yellow = (52, 99, -35, 11, 34, 101)
bi_threshold = (178, 255)

# 定义变量
Q = 'd'
benchmark_send = ''
send_map = 0
k = 0
findrect_flag = 0

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.7)


#绿灯闪烁证明程序运行中----------------------------------------------------------------------
    green.toggle()

#识别地图任务-------------------------------------------------------------------------------
    if Q == 'd':
        #img.gaussian(1)
        img.binary([bi_threshold], invert = 1)
        for r in img.find_rects(threshold = 50000):             # 在图像中搜索矩形
            map = []
            # 识别到矩形ROI区域的信息
            xr = r.rect()[0]
            yr = r.rect()[1]
            w  = r.rect()[2]
            h  = r.rect()[3]
            #if (w >=130 and w <=260 and h >= 80 and h <= 180):

            img.draw_rectangle(r.rect(), color = (255, 0, 0),thickness = 1)   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
            #print_rect = (xr, yr, w, h)
            #print("Rect: xr: %f, yr: %f, w: %f, h: %f" % print_rect)
            for c in img.find_circles(roi = r.rect(),threshold = 2300, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max = 4, r_step = 5):
                img.draw_circle(c.x() , c.y() , c.r(), color = (255, 0, 0),thickness = 2)

                #k = (xr + w)/700 #虚拟地图和实际地图的比例 （小于1），单位：cm
                #print_point = (c.x(), c.y(), c.r())
                #print("Point: x: %f, y: %f, r: %f" % print_point)

                pi_x = int(((c.x() - xr)/w) * 35)+1  # （（点虚拟距离/地图虚拟边长）* 格子数量 ）+1  根据实测发现大部分坐标少了1，因此强行调整+1
                pi_y = int(((yr + h - c.y())/h) * 25)+1
                map.append(pi_x)
                map.append(pi_y)
                #img.draw_string(c.x() , c.y(), "({},{})".format(pi_x,pi_y), color = (0, 0, 255), scale = 2)
            print(map)

            if send_map == 1:
                for i in range(0, len(map), 2):
                    uart2.write("{:0>2}XZ{:0>2}YZ".format(map[i],map[i+1]))
                Q = "r"

#调整基准值任务-------------------------------------------------------------------------------
    if Q == 'b':
        img.binary([yellow], invert = 0)

        findrect_flag = 0
        for r in img.find_rects(threshold = 100000):
            img1 = img.copy(r.rect())
            #print(clock.fps())
            img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
            #print(r.rect())
            #print(r.corners())
            # r.corners()返回二维元组，从左下角开始为第一个点逆时针依次存储
            findrect_flag = 1
            yr = r.corners()[0][1] - r.corners()[3][1]
            xr = r.corners()[3][0] - r.corners()[0][0]

            yl = r.corners()[0][1] - r.corners()[1][1]
            xl = r.corners()[1][0] - r.corners()[0][0]
            #i = 0
            #for p in r.corners():
                #i = i +1
                #img.draw_string(p[0], p[1], str(i), color = (255,0,0), scale = 2)
                #img.draw_cross(p[0], p[1], 5, color = (0, 255, 0))
            if xl and xr:
                if abs(yr/xr)<0.8:
                    k = yr/xr
                elif abs(yl/xl)<0.8:
                    k = yl/xl
                else:
                    k = 0
        if findrect_flag == 0:
            k = 0

        #yellow_blobs = img.find_blobs([yellow], merge=True)
        #for blob in yellow_blobs:
            #img.draw_rectangle(blob.rect(), color = (255, 0, 0))
            #print(blob.rotation())

        # 精度为0.001
        #benchmark_send = str(int(k * 100))
        #uart2.write("{:0>3}bZ".format(benchmark_send))
        #print("{:0>3}bZ".format(benchmark_send))

        # 精度为0.01
        benchmark_send = str(int(k * 10))
        uart1.write("{:0>2}bZ".format(benchmark_send))
        print("{:0>2}bZ".format(benchmark_send))
        print(clock.fps())

