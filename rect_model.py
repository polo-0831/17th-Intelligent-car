import pyb
import sensor, image, time, math
import os, tf
from machine import UART
from pyb import LED
uart = UART(2, baudrate=115200)     # 初始化串口 波特率设置为115200 TX是B12 RX是B13

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.HQVGA) #HQVGA:240x160
sensor.set_brightness(2500)
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False,(0,0x80,0))  # must turn this off to prevent image washout...
clock = time.clock()

net_path = "mobilenet_v2-new_shot_0.86acc.tflite"                                  # 定义模型的路径
labels = [line.rstrip() for line in open("/sd/labels_animal_fruits_vehicle.txt")]   # 加载标签
net = tf.load(net_path, load_to_fb=True)                                  # 加载模型

# 定义模型标签类别
animals = ['dog', 'horse', 'cat', 'cattle', 'pig']
fruits = ['orange', 'apple', 'durian', 'grape', 'banana']
vehicle = ['train', 'ship', 'plane', 'car', 'bus']


# 定义中心坐标数组
center = [0, 0] #240x160内的像素坐标


# 定义标志位
#Q = 'n'
while(True):
    clock.tick()


    #if(uart.any()): # 返回等待的字节数量
        #uart_str = uart.readline().strip()
        ##uart.write(uart_str)    # 将读取到的串口数据发回
        #if uart_str == b'r': # 识别矩形
            ##print(uart_str)
            #Q = 'r'
        #elif uart_str == b'm': # 运行模型识别
            ##print(uart_str)
            #Q = 'm'
        #elif uart_str == b'n': # 啥都不干
            ##print(uart_str)
            #Q = 'n'


    #print(Q)
    img = sensor.snapshot().lens_corr(1.8)

    #if Q == 'r':
    for r in img.find_rects(threshold = 50000):             # 在图像中搜索矩形
        img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
        #print(r.rect())
        uart.write('a')
        #img.draw_cross(int(r.rect()[0]+r.rect()[2]/2), int(r.rect()[1]+r.rect()[3]/2), color = (0, 255, 0), size = 2, thickness = 1)
        #center[0] = int(r.rect()[0]+r.rect()[2]/2)
        #center[1] = int(r.rect()[1]+r.rect()[3]/2)
        #for i, element in enumerate(center):
            #uart.write(str(element))
            #if(i == 0):
                #uart.write('x')
            #if(i == 1):
                #uart.write('y\r\n')


    #if Q == 'm':
        #for r in img.find_rects(threshold = 50000):
            #img1 = img.copy(r.rect())
            ##print(clock.fps())
            #img.draw_rectangle(r.rect(), color = (255, 0, 0))   # 绘制矩形外框，便于在IDE上查看识别到的矩形位置
            ##print(r.rect())

            #for obj in tf.classify(net , img1, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
                #print("**********\nTop 1 Detections at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
                #sorted_list = sorted(zip(labels, obj.output()), key = lambda x: x[1], reverse = True)
                ## 打印准确率最高的结果
                #for i in range(1):
                    #print("%s = %f" % (sorted_list[i][0], sorted_list[i][1]))
                    #if(sorted_list[i][0] in animals):
                        #if(sorted_list[i][0] == animals[0]):
                            #print(animals[0])
                            #uart.write("11\r\n")
                        #elif(sorted_list[i][0] == animals[1]):
                            #print(animals[1])
                            #uart.write("12\r\n")
                        #elif(sorted_list[i][0] == animals[2]):
                            #print(animals[2])
                            #uart.write("13\r\n")
                        #elif(sorted_list[i][0] == animals[3]):
                            #print(animals[3])
                            #uart.write("14\r\n")
                        #elif(sorted_list[i][0] == animals[4]):
                            #print(animals[4])
                            #uart.write("15\r\n")
                    #elif(sorted_list[i][0] in fruits):
                        #if(sorted_list[i][0] == fruits[0]):
                            #print(fruits[0])
                            #uart.write("21\r\n")
                        #elif(sorted_list[i][0] == fruits[1]):
                            #print(fruits[1])
                            #uart.write("22\r\n")
                        #elif(sorted_list[i][0] == fruits[2]):
                            #print(fruits[2])
                            #uart.write("23\r\n")
                        #elif(sorted_list[i][0] == fruits[3]):
                            #print(fruits[3])
                            #uart.write("24\r\n")
                        #elif(sorted_list[i][0] == fruits[4]):
                            #print(fruits[4])
                            #uart.write("25\r\n")
                    #elif(sorted_list[i][0] in vehicle):
                        #if(sorted_list[i][0] == vehicle[0]):
                            #print(vehicle[0])
                            #uart.write("31\r\n")
                        #elif(sorted_list[i][0] == vehicle[1]):
                            #print(vehicle[1])
                            #uart.write("32\r\n")
                        #elif(sorted_list[i][0] == vehicle[2]):
                            #print(vehicle[2])
                            #uart.write("33\r\n")
                        #elif(sorted_list[i][0] == vehicle[3]):
                            #print(vehicle[3])
                            #uart.write("34\r\n")
                        #elif(sorted_list[i][0] == vehicle[4]):
                            #print(vehicle[4])
                            #uart.write("35\r\n")
