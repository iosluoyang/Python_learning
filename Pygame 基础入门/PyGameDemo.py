# -*- coding: utf-8 -*-
import  pygame
from pygame.locals import *

def main():
    # 创建窗口
    screen = pygame.display.set_mode((480,800))
    # 设置窗口名称
    pygame.display.set_caption('刘海洋的第一个打飞机游戏')
    #创建clock对象
    clock = pygame.time.Clock()

    #加载所需的图像资源
    bg = pygame.image.load('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Pygame 基础入门/images/background.png').convert()
    plane = pygame.image.load('/Users/HelloWorld/Documents/个人相关/TobeBetterMe/Python学习进程/Pygame 基础入门/images/plane.png').convert_alpha()


    #程序逻辑主体
    while True:
        #设置帧数为30
        clock.tick(30)
        #绘制背景
        screen.blit(bg,(0,0))
        #获取鼠标坐标
        (x,y) = pygame.mouse.get_pos()
        #分别获取图像宽高
        x -= plane.get_width() / 2
        y -= plane.get_height() / 2
        #绘制飞机
        screen.blit(plane,(x,y))

        #遍历处理事件
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        #更新画面
            pygame.display.update()



if __name__ == '__main__':
    main()


