# -*- coding: utf-8 -*-
from PIL import Image
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output')   #输出文件
parser.add_argument('--width', type = int, default = 80) #输出字符画宽
parser.add_argument('--height', type = int, default = 80) #输出字符画高

#获取参数
args = parser.parse_args()

IMG = 'picdemo.png'
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
# RGB值转字符的函数：
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

if __name__ == '__main__':

    #打开图片
    im = Image.open(IMG)
    #将图片缩放至指定尺寸
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

    txt = ""
    #先找出像素点所在位置的RGB值，然后在每一横行找到相应的文字拼接，在每一竖行上增加一个回车
    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)

    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Python图片转字符画/output.txt",'w') as f:
            f.write(txt)