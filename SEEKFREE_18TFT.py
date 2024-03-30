from machine import SPI,Pin
import time, sensor, image

# IO接线方法
# 屏         openart
# GND       ---> GND
# VCC       ---> 3.3V
# SCL       ---> B0(SCLK)
# SDA/MISO  ---> B1(MISO)
# RESET     ---> B12
# DC        ---> B13
# CS        ---> B3
# BL        ---> B16 (背光控制)

#字符字典
asc ={
       "0":[0x00,0x00,0x00,0x18,0x24,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00,0x00],
       "1":[0x00,0x00,0x00,0x10,0x1C,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x7C,0x00,0x00],
       "2":[0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x40,0x20,0x10,0x08,0x04,0x42,0x7E,0x00,0x00],
       "3":[0x00,0x00,0x00,0x3C,0x42,0x42,0x40,0x20,0x18,0x20,0x40,0x42,0x42,0x3C,0x00,0x00],
       "4":[0x00,0x00,0x00,0x20,0x30,0x30,0x28,0x24,0x24,0x22,0xFE,0x20,0x20,0xF8,0x00,0x00],
       "5":[0x00,0x00,0x00,0x7E,0x02,0x02,0x02,0x1E,0x22,0x40,0x40,0x42,0x22,0x1C,0x00,0x00],
       "6":[0x00,0x00,0x00,0x18,0x24,0x02,0x02,0x3A,0x46,0x42,0x42,0x42,0x44,0x38,0x00,0x00],
       "7":[0x00,0x00,0x00,0x7E,0x42,0x20,0x20,0x10,0x10,0x08,0x08,0x08,0x08,0x08,0x00,0x00],
       "8":[0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x24,0x18,0x24,0x42,0x42,0x42,0x3C,0x00,0x00],
       "9":[0x00,0x00,0x00,0x1C,0x22,0x42,0x42,0x42,0x62,0x5C,0x40,0x40,0x24,0x18,0x00,0x00],
       "A":[0x00,0x00,0x00,0x08,0x08,0x18,0x14,0x14,0x24,0x3C,0x22,0x42,0x42,0xE7,0x00,0x00],
       "B":[0x00,0x00,0x00,0x1F,0x22,0x22,0x22,0x1E,0x22,0x42,0x42,0x42,0x22,0x1F,0x00,0x00],
       "C":[0x00,0x00,0x00,0x7C,0x42,0x42,0x01,0x01,0x01,0x01,0x01,0x42,0x22,0x1C,0x00,0x00],
       "D":[0x00,0x00,0x00,0x1F,0x22,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x22,0x1F,0x00,0x00],
       "E":[0x00,0x00,0x00,0x3F,0x42,0x12,0x12,0x1E,0x12,0x12,0x02,0x42,0x42,0x3F,0x00,0x00],
       "F":[0x00,0x00,0x00,0x3F,0x42,0x12,0x12,0x1E,0x12,0x12,0x02,0x02,0x02,0x07,0x00,0x00],
       "G":[0x00,0x00,0x00,0x3C,0x22,0x22,0x01,0x01,0x01,0x71,0x21,0x22,0x22,0x1C,0x00,0x00],
       "H":[0x00,0x00,0x00,0xE7,0x42,0x42,0x42,0x42,0x7E,0x42,0x42,0x42,0x42,0xE7,0x00,0x00],
       "I":[0x00,0x00,0x00,0x3E,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,0x00],
       "J":[0x00,0x00,0x00,0x7C,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x11,0x0F],
       "K":[0x00,0x00,0x00,0x77,0x22,0x12,0x0A,0x0E,0x0A,0x12,0x12,0x22,0x22,0x77,0x00,0x00],
       "L":[0x00,0x00,0x00,0x07,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x42,0x7F,0x00,0x00],
       "M":[0x00,0x00,0x00,0x77,0x36,0x36,0x36,0x36,0x36,0x2A,0x2A,0x2A,0x2A,0x6B,0x00,0x00],
       "N":[0x00,0x00,0x00,0xE3,0x46,0x46,0x4A,0x4A,0x52,0x52,0x52,0x62,0x62,0x47,0x00,0x00],
       "O":[0x00,0x00,0x00,0x1C,0x22,0x41,0x41,0x41,0x41,0x41,0x41,0x41,0x22,0x1C,0x00,0x00],
       "P":[0x00,0x00,0x00,0x3F,0x42,0x42,0x42,0x42,0x3E,0x02,0x02,0x02,0x02,0x07,0x00,0x00],
       "Q":[0x00,0x00,0x00,0x1C,0x22,0x41,0x41,0x41,0x41,0x41,0x41,0x4D,0x32,0x1C,0x60,0x00],
       "R":[0x00,0x00,0x00,0x3F,0x42,0x42,0x42,0x3E,0x12,0x12,0x22,0x22,0x42,0xC7,0x00,0x00],
       "S":[0x00,0x00,0x00,0x7C,0x42,0x42,0x02,0x04,0x18,0x20,0x40,0x42,0x42,0x3E,0x00,0x00],
       "T":[0x00,0x00,0x00,0x7F,0x49,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x1C,0x00,0x00],
       "U":[0x00,0x00,0x00,0xE7,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x3C,0x00,0x00],
       "V":[0x00,0x00,0x00,0xE7,0x42,0x42,0x22,0x24,0x24,0x14,0x14,0x18,0x08,0x08,0x00,0x00],
       "W":[0x00,0x00,0x00,0x6B,0x2A,0x2A,0x2A,0x2A,0x2A,0x36,0x14,0x14,0x14,0x14,0x00,0x00],
       "X":[0x00,0x00,0x00,0xE7,0x42,0x24,0x24,0x18,0x18,0x18,0x24,0x24,0x42,0xE7,0x00,0x00],
       "Y":[0x00,0x00,0x00,0x77,0x22,0x22,0x14,0x14,0x08,0x08,0x08,0x08,0x08,0x1C,0x00,0x00],
       "Z":[0x00,0x00,0x00,0x7E,0x21,0x20,0x10,0x10,0x08,0x04,0x04,0x42,0x42,0x3F,0x00,0x00],
       "a":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1C,0x22,0x30,0x2C,0x22,0x32,0x6C,0x00,0x00],
       "b":[0x00,0x00,0x00,0x00,0x03,0x02,0x02,0x1A,0x26,0x42,0x42,0x42,0x26,0x1A,0x00,0x00],
       "c":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x38,0x44,0x02,0x02,0x02,0x44,0x38,0x00,0x00],
       "d":[0x00,0x00,0x00,0x00,0x60,0x40,0x40,0x7C,0x42,0x42,0x42,0x42,0x62,0xDC,0x00,0x00],
       "e":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3C,0x42,0x42,0x7E,0x02,0x42,0x3C,0x00,0x00],
       "f":[0x00,0x00,0x00,0x00,0x30,0x48,0x08,0x3E,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,0x00],
       "g":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7C,0x22,0x22,0x1C,0x02,0x3C,0x42,0x42,0x3C],
       "h":[0x00,0x00,0x00,0x00,0x03,0x02,0x02,0x3A,0x46,0x42,0x42,0x42,0x42,0xE7,0x00,0x00],
       "i":[0x00,0x00,0x00,0x0C,0x0C,0x00,0x00,0x0E,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,0x00],
       "j":[0x00,0x00,0x00,0x30,0x30,0x00,0x00,0x38,0x20,0x20,0x20,0x20,0x20,0x20,0x22,0x1E],
       "k":[0x00,0x00,0x00,0x00,0x03,0x02,0x02,0x72,0x12,0x0A,0x0E,0x12,0x22,0x77,0x00,0x00],
       "l":[0x00,0x00,0x00,0x08,0x0E,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,0x00],
       "m":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7F,0x92,0x92,0x92,0x92,0x92,0xB7,0x00,0x00],
       "n":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3B,0x46,0x42,0x42,0x42,0x42,0xE7,0x00,0x00],
       "o":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x42,0x42,0x3C,0x00,0x00],
       "p":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1B,0x26,0x42,0x42,0x42,0x26,0x1A,0x02,0x07],
       "q":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x58,0x64,0x42,0x42,0x42,0x64,0x58,0x40,0xE0],
       "r":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x77,0x4C,0x04,0x04,0x04,0x04,0x1F,0x00,0x00],
       "s":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7C,0x42,0x02,0x3C,0x40,0x42,0x3E,0x00,0x00],
       "t":[0x00,0x00,0x00,0x00,0x00,0x08,0x08,0x3E,0x08,0x08,0x08,0x08,0x48,0x30,0x00,0x00],
       "u":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x63,0x42,0x42,0x42,0x42,0x62,0xDC,0x00,0x00],
       "v":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x77,0x22,0x22,0x14,0x14,0x08,0x08,0x00,0x00],
       "w":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xDB,0x91,0x52,0x5A,0x2A,0x24,0x24,0x00,0x00],
       "x":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x6E,0x24,0x18,0x18,0x18,0x24,0x76,0x00,0x00],
       "y":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE7,0x42,0x24,0x24,0x18,0x18,0x08,0x08,0x06],
       "z":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7E,0x22,0x10,0x08,0x08,0x44,0x7E,0x00,0x00],
       " ":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
       ".":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x06,0x06,0x00,0x00],
       "-":[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7E,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    }

cs  = Pin(("B3",  3))    #引脚定义 TFT CS引脚接B3
rst = Pin(("B12", 12))   #引脚定义 TFT RES引脚接B12
dc  = Pin(("B13", 13))   #引脚定义 TFT DC引脚接B13
bl  = Pin(("B16", 16))   #引脚定义 TFT BL引脚接B16
spi = SPI(30)  #创建对象 SPI3总线上的第0个设备

#定义显示方向
#0 竖屏模式
#1 竖屏模式  旋转180
#2 横屏模式
#3 横屏模式  旋转180
TFT_DISPLAY_DIR = 2;

X_MAX_PIXEL = 0
Y_MAX_PIXEL = 0
if (0==TFT_DISPLAY_DIR):
    X_MAX_PIXEL = 128               # 定义屏幕宽度
    Y_MAX_PIXEL = 160               # 定义屏幕高度
elif (1==TFT_DISPLAY_DIR):
    X_MAX_PIXEL = 128               # 定义屏幕宽度
    Y_MAX_PIXEL = 160               # 定义屏幕高度
elif (2==TFT_DISPLAY_DIR):
    X_MAX_PIXEL = 160               # 定义屏幕宽度
    Y_MAX_PIXEL = 128               # 定义屏幕高度
elif (3==TFT_DISPLAY_DIR):
    X_MAX_PIXEL = 160               # 定义屏幕宽度
    Y_MAX_PIXEL = 128               # 定义屏幕高度

# 常用颜色表
RED     = 0XF800
GREEN   = 0X07E0
BLUE    = 0X001F
BLACK   = 0X0000
YELLOW  = 0XFFE0
WHITE   = 0XFFFF
CYAN    = 0X07FF
BRIGHT_RED = 0XF810
GRAY1   = 0X8410
GRAY2   = 0X4208

# 定义笔刷
TFT_PENCOLOR = RED
# 定义背景
TFT_BGCOLOR = WHITE

# TFT初始化
def tft_init():
    dc.init(Pin.OUT_PP, Pin.PULL_NONE)  #引脚初始化，方向：输出 无上拉
    rst.init(Pin.OUT_PP, Pin.PULL_NONE) #引脚初始化，方向：输出 无上拉
    cs.init(Pin.OUT_PP, Pin.PULL_NONE)  #引脚初始化，方向：输出 无上拉
    bl.init(Pin.OUT_PP, Pin.PULL_NONE)  #引脚初始化，方向：输出 无上拉 背光控制
    
    spi.init(30000000,0,0,8,SPI.MSB)#初始化 波特率30000000，极性0，相位0，传输数据长度8位，从高位开始传输数据
    
    bl.value(1)
    rst.value(0)
    time.sleep(100)
    rst.value(1)
    time.sleep(100)
    write_command(0x11)
    time.sleep(100)
    write_command(0xB1, 0x01, 0x2C, 0x2D)
    write_command(0xB2, 0x01, 0x2C, 0x2D)
    write_command(0xB3, 0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D)
    write_command(0xB4, 0x07)
    write_command(0xC0, 0xA2, 0x02, 0x84)
    write_command(0xC1, 0xC5)
    write_command(0xC2, 0x0A, 0x00)
    write_command(0xC3, 0x8A, 0x2A)
    write_command(0xC4, 0x8A, 0xEE)
    write_command(0xC5, 0x0E)
    if (0==TFT_DISPLAY_DIR):
        write_command(0x36, 0xC0)
    elif (1==TFT_DISPLAY_DIR):
        write_command(0x36, 0x00)
    elif (2==TFT_DISPLAY_DIR):
        write_command(0x36, 0xA0)
    elif (3==TFT_DISPLAY_DIR):
        write_command(0x36, 0x60)
    write_command(0xE0, 0x0F, 0x1A, 0x0F, 0x18, 0x2F, 0x28, 0x20, 0x22, 0x1f, 0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10)
    write_command(0XE1, 0x0F, 0x1B, 0x0F, 0x17, 0x33, 0x2C, 0x29, 0x2E, 0x30, 0x30, 0x39, 0x3F, 0x00, 0x07, 0x03, 0x10)
    write_command(0x2A, 0x00, 0x02, 0x00, 0x82)
    write_command(0x2B, 0x00, 0x03, 0x00, 0x83)
    write_command(0xF0, 0x01)
    write_command(0xF6, 0x00)
    write_command(0x3A, 0x05)
    write_command(0x29)
    tft_clear(TFT_BGCOLOR)

# 写命令
def write_command_byte(c):
    c = c.to_bytes(1,'little')
    cs.value(0)
    dc.value(0)
    spi.write(c)
    cs.value(1)

# 写8位数据
def write_data_byte(c):
    c = c.to_bytes(1,'little')
    cs.value(0)
    dc.value(1)
    spi.write(c)
    cs.value(1)

# 写16位数据
def write_data_16bit(dat):
    write_data_byte(dat >> 8)
    write_data_byte(dat&0xFF)

# 写命令
def write_command(c, *data):
    write_command_byte(c)
    if data:
        for d in data:
            if d > 255:
                write_data_byte(d >> 8)
                write_data_byte(d&0xFF)
            else:
                write_data_byte(d)

# 框选坐标
def tft_set_region(x_start, y_start, x_end, y_end):
    if 0==TFT_DISPLAY_DIR:
        write_command(0x2A, 0x00, x_start+2, 0x00, x_end+2)
        write_command(0x2B, 0x00, y_start+1, 0x00, y_end+1)
    elif 1==TFT_DISPLAY_DIR:
        write_command(0x2A, 0x00, x_start+2, 0x00, x_end+2)
        write_command(0x2B, 0x00, y_start+1, 0x00, y_end+1)
    elif 2==TFT_DISPLAY_DIR:
        write_command(0x2A, 0x00, x_start+1, 0x00, x_end+1)
        write_command(0x2B, 0x00, y_start+2, 0x00, y_end+2)
    elif 3==TFT_DISPLAY_DIR:
        write_command(0x2A, 0x00, x_start+1, 0x00, x_end+1)
        write_command(0x2B, 0x00, y_start+2, 0x00, y_end+2)
    write_command(0x2C)

# 设置坐标
def tft_set_xy(xpos, ypos):
    tft_set_region(xpos, ypos, xpos, ypos)

# 在指定位置绘制一个点
def tft_drawpoint(x, y, Color):
    tft_set_xy(x, y)
    write_data_byte(Color >> 8)
    write_data_byte(Color&0XFF)

# 显示字符
def tft_showchar(x,y,s):

    if x > X_MAX_PIXEL-7: x = X_MAX_PIXEL-7
    if y > (int)(Y_MAX_PIXEL/16): y = (int)(Y_MAX_PIXEL/16)
    p=0
    bit8=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
    for i in asc[s]:
        tft_set_region(x,(y-1)*16+p,x+7,(y-1)*16+p)
        for j in bit8:
            if i&j :
                write_data_16bit(TFT_PENCOLOR)
            else:
                write_data_16bit(TFT_BGCOLOR)
        p+=1

# 显示字符串
def tft_showstr(x,y,strd):
    j = 0
    for i in strd:
        tft_showchar(x+8*j,y,i)
        j+=1

# 显示数字
def tft_shownum(x,y,dat):
    tft_showstr(x,y,str(dat))

# 清屏
def tft_clear(Color):
    tft_set_region(0, 0, X_MAX_PIXEL - 1, Y_MAX_PIXEL - 1)
    for i in range(0, Y_MAX_PIXEL):
        for m in range(0, X_MAX_PIXEL):
            write_data_byte(Color >> 8)
            write_data_byte(Color&0xFF)

# 显示图像
def tft_display(image,sizeX,szeY):
    tft_set_region(0, 0,sizeX-1,szeY-1)
    cs.value(0)
    dc.value(1)
    spi.write(image)
    cs.value(1)

# 图像上显示字符串
#image 获取的图像截图
#x 显示的x位置
#y 显示的y位置
#s 需要显示的字符
#r,g,b 需要显示字符的颜色

def tft_display_string_in_image(image,x,y,s,r,g,b):
    image.draw_string(x, y, s, color = (r, g, b), scale = 2, mono_space = False,
                char_rotation = 0, char_hmirror = False, char_vflip = False,
                string_rotation = 0, string_hmirror = False, string_vflip = False)

