import pyb
import sensor, image, time, math
import os, tf
from machine import UART
from pyb import LED
#import SEEKFREE_IPS114_SPI as ips114
import SEEKFREE_18TFT as tft18
#import SEEKFREE_IPS114_SPI as ips114
# 初始化串口 波特率设置为115200 TX是B12 RX是B13
uart2 = UART(2, baudrate=115200)

LED(4).on()
green = LED(2)  # 定义一个LED2   绿灯
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) #QQVGA:240x160
sensor.set_brightness(500)
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
tft18.tft_init()
clock = time.clock()

net_path = "7mobilenet_v2-offlineaug_shot_acc0.942_100batch_29epoch.tflite"   # 定义模型的路径
labels = [line.rstrip() for line in open("/sd/labels_animal_fruits_vehicle.txt")]   # 加载标签
net = tf.load(net_path, load_to_fb=True)                                  # 加载模型

# 定义模型标签类别
animals = ['dog', 'horse', 'cat', 'cattle', 'pig']
fruits = ['orange', 'apple', 'durian', 'grape', 'banana']
vehicle = ['train', 'ship', 'plane', 'car', 'bus']


# 定义中心坐标数组
center = [0, 0] #160x120内的像素坐标
yellow = (52, 99, -35, 11, 11, 116) # 亮的
bi_threshold = (74, 100, -3, 10, -26, 7)

# 定义变量
Q = 'd'
model_send = ''
benchmark_send = ''
send_map = 0
k = 0
findrect_flag = 0
map = []
circle_threshold = 800
blob_mode = 1

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    if blob_mode == 1:
        yellow = (52, 99, -35, 11, 11, 116)
    elif blob_mode == 2:
        yellow = (41, 100, -58, -2, 18, 79)

#绿灯闪烁证明程序运行中----------------------------------------------------------------------
    green.toggle()

#接受任务字----------------------------------------------------------------------------------
    if(uart2.any()): # 返回等待的字节数量
        uart_str = uart2.readline().strip().decode()
        #print(uart_str)

        #uart_str是byte型变量为b''，用decode方法转换为字符串格式变量
        #uart.write(uart_str)    # 将读取到的串口数据发回
        if uart_str == 'r': # 识别矩形
            Q = 'r'
        elif uart_str == 'm': # 运行模型识别和0度纠正
            Q = 'm'
        elif uart_str == 'd': # 运行地图识别
            Q = 'd'
        elif uart_str == 'b': # 基准值调整
            Q = 'b'
        elif uart_str == 's': # 发送地图信息flag
            send_map = 1
        elif uart_str == 'c': # 圆阈值
            circle_threshold = circle_threshold + 20
        elif uart_str == 'g':
            circle_threshold = circle_threshold - 20
        elif uart_str == 'e': # 色块模式：正常/暗
            blob_mode = blob_mode + 1
            if blob_mode > 2:
                blob_mode = 1

        #print(Q)


#调整基准值任务-------------------------------------------------------------------------------
    if Q == 'b':
        #img.gaussian(5)

        img.binary([yellow], invert = 0)
        findrect_flag = 0
        for r in img.find_rects(threshold = 200000):
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
            if xl or xr:
                if abs(yr/xr)<0.9:
                    k = yr/xr
                elif abs(yl/xl)<0.9:
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
        uart2.write("{:0>2}bZ".format(benchmark_send))
        print("{:0>2}bZ".format(benchmark_send))
        #print(clock.fps())


#识别地图任务-------------------------------------------------------------------------------
    if Q == 'd':
        #img.gaussian(gaussin)
        #img.binary([bi_threshold], invert = 1)
        for r in img.find_rects(threshold = 50000):             # 在图像中搜索矩形
            map = []
            # 识别到矩形ROI区域的信息
            xr = r.rect()[0]
            yr = r.rect()[1]
            w  = r.rect()[2]
            h  = r.rect()[3]
            if (w >=200 and w <=320 and h >= 130 and h <= 240):

                img.draw_rectangle(r.rect(), color = (255, 0, 0),thickness = 3)   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
                #img1 = img.copy(r.rect())                           # 提取矩形内ROI区域


                #print_rect = (xr, yr, w, h)
                #print("Rect: xr: %f, yr: %f, w: %f, h: %f" % print_rect)
                for c in img.find_circles(roi = r.rect(),threshold = circle_threshold, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max = 6, r_step = 5):

                    img.draw_circle(c.x() , c.y() , c.r(), color = (255, 0, 0),thickness = 2)

                    #k = (xr + w)/700 #虚拟地图和实际地图的比例 （小于1），单位：cm
                    #print_point = (c.x(), c.y(), c.r())
                    #print("Point: x: %f, y: %f, r: %f" % print_point)

                    pi_x = int(((c.x() - xr)/w) * 35)+1  # （（点虚拟距离/地图虚拟边长）* 格子数量 ）+1  根据实测发现大部分坐标少了1，因此强行调整+1
                    pi_y = int(((yr + h - c.y ())/h) * 25)+1
                    if pi_x >= 30 and pi_x <= 32:
                        pi_x = pi_x + 1
                    if not (pi_x >= 34 or pi_x <=1 or pi_y >= 24 or pi_y <= 1):
                        map.append(pi_x)
                        map.append(pi_y)
                    #img.draw_string(c.x() , c.y(), "({},{})".format(pi_x,pi_y), color = (0, 0, 255), s cale = 2)
                print(map)
                tft18.tft_display_string_in_image(img,20,60,str(len(map)/2),255,0,0)
                tft18.tft_display_string_in_image(img,20,80,str(circle_threshold),255,0,0)
                tft18.tft_display_string_in_image(img,20,100,str(blob_mode),255,0,0)

                if send_map == 1:
                    for i in range(0, len(map), 2):
                        uart2.write("{:0>2}XZ{:0>2}YZ".format(map[i],map[i+1]))
                    Q = "r"
        tft18.tft_display(img.crop([0,0,320,240], 0.5, 0.5),160,120)

#微调任务-------------------------------------------------------------------------------
    if Q == 'r':
        yellow_blobs = img.find_blobs([yellow], merge=True)
        cx = 0
        cy = 0
        w = 0
        h = 0
        for i in yellow_blobs:
            img.draw_rectangle(i.rect(), color = (255, 0, 0))

            cx = max(i.cx(),cx)
            cy = max(i.cy(),cy)
            w = max(i.w(),w)
            h = max(i.h(),h)
            img.draw_circle(cx, cy, 2, color = (0,0,255), thickness = 2, fill = True)
        if (cx and cy):
            uart2.write("{:0>3}x{:0>3}y{:0>3}w{:0>3}hZ".format(cx, cy, w, h))
            print("{:0>3}x{:0>3}y{:0>3}w{:0>3}hZ".format(cx, cy, w, h))



#模型识别任务----------------------------------------------------------------------------------------------
    if Q == 'm':
        for r in img.find_rects(threshold = 50000):
            img1 = img.copy(r.rect())
            #print(clock.fps())
            img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
            #print(r.rect())
            #print(r.corners())

            # r.corners()返回二维元组，从左下角开始为第一个点逆时针依次存储
            y = r.corners()[0][1] - r.corners()[3][1]
            x = r.corners()[3][0] - r.corners()[0][0]
            if not x==0 and abs(int(y/x))<20:
                benchmark_send = str(int(y/x))
            else:
                benchmark_send = "000"

            for obj in tf.classify(net , img1, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
                print("**********\nTop 1 Detections at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
                sorted_list = sorted(zip(labels, obj.output()), key = lambda x: x[1], reverse = True)
                # 打印准确率最高的结果
                for i in range(1):
                    print("%s = %f" % (sorted_list[i][0], sorted_list[i][1]))
                    if(sorted_list[i][0] in animals):
                        if(sorted_list[i][0] == animals[0]):
                            #print(animals[0])
                            model_send = "011"
                            #uart1.write("011mZ")
                        elif(sorted_list[i][0] == animals[1]):
                            #print(animals[1])
                            model_send = "012"
                            #uart1.write("012mZ")
                        elif(sorted_list[i][0] == animals[2]):
                            #print(animals[2])
                            model_send = "013"
                            #uart1.write("013mZ")
                        elif(sorted_list[i][0] == animals[3]):
                            #print(animals[3])
                            model_send = "014"
                            #uart1.write("014mZ")
                        elif(sorted_list[i][0] == animals[4]):
                            #print(animals[4])
                            model_send = "015"
                            #uart1.write("015mZ")
                    elif(sorted_list[i][0] in fruits):
                        if(sorted_list[i][0] == fruits[0]):
                            #print(fruits[0])
                            model_send = "021"
                            #uart1.write("021mZ")
                        elif(sorted_list[i][0] == fruits[1]):
                            #print(fruits[1])
                            model_send = "022"
                            #uart1.write("022mZ")
                        elif(sorted_list[i][0] == fruits[2]):
                            #print(fruits[2])
                            model_send = "023"
                            #uart1.write("023mZ")
                        elif(sorted_list[i][0] == fruits[3]):
                            #print(fruits[3])
                            model_send = "024"
                            #uart1.write("024mZ")
                        elif(sorted_list[i][0] == fruits[4]):
                            #print(fruits[4])
                            model_send = "025"
                            #uart1.write("025mZ")
                    elif(sorted_list[i][0] in vehicle):
                        if(sorted_list[i][0] == vehicle[0]):
                            #print(vehicle[0])
                            model_send = "031"
                            #uart1.write("031mZ")
                        elif(sorted_list[i][0] == vehicle[1]):
                            #print(vehicle[1])
                            model_send = "032"
                            #uart1.write("032mZ")
                        elif(sorted_list[i][0] == vehicle[2]):
                            #print(vehicle[2])
                            model_send = "033"
                            #uart1.write("033mZ")
                        elif(sorted_list[i][0] == vehicle[3]):
                            #print(vehicle[3])
                            model_send = "034"
                        elif(sorted_list[i][0] == vehicle[4]):
                            #print(vehicle[4])
                            model_send = "035"
            uart2.write(model_send + "mZ")
            print(model_send + "mZ")



