from machine import UART
import pyb
import struct
from pyb import LED
import sensor, image, utime, math, tf
import os

LED(4).on()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # we run out of memory if the resolution is much bigger...
sensor.set_brightness(1200)
sensor.skip_frames(time = 20)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
#clock = time.clock()



save_img_num = 0;
start = utime.ticks_ms()  # get value of millisecond counter  获取毫秒计数器的值
while(True):
    img = sensor.snapshot().lens_corr(1.8)
    delta = utime.ticks_diff(utime.ticks_ms(), start)  # compute time difference 计算时间差
    if delta > 350:
        for r in img.find_rects(threshold = 50000):
            img1 = img.copy(r.rect())
            save_img_num += 1;
            print(save_img_num)
            image_pat = "/photos/"+str(save_img_num)+".jpg"
            img1.save(image_pat,quality=100)
            start = utime.ticks_ms()  # get value of millisecond counter  获取毫秒计数器的值
