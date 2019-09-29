#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
from random import *
import math

class Bonus(pygame.sprite.Sprite):    # 继承
    def __init__(self,ratio,x,y,screen_size,type=0,num=0):    #,speed=None,mode=None,move=None
        pygame.sprite.Sprite.__init__(self)
        
        self.die_timer = 60*15
        self.flashing = False
        self.active = True
        self.type = type    # 0子弹数量，1子弹类型，2僚机，3大招，4血，5蓝
        self.num = num
        self.ratio = ratio
        
        # 传入bg的参数做限制
        self.width = screen_size[0]
        self.height = screen_size[1]
        
        # 运动
        self.aim = (randint(int(screen_size[0]*4/10),int(screen_size[0]*6/10)),\
                    randint(int(screen_size[1]*4/10),int(screen_size[1]*6/10)))
        self.real_center_x = x
        self.real_center_y = y
        
        # 旋转
        self.degree = self.get_aim_degree()
        
        # 设定移动的方向和速度
        speed = 3
        self.raw_speed_x = speed*math.sin(self.degree)*randint(50,100)/100
        self.raw_speed_y = speed*math.cos(self.degree)*randint(50,100)/100
        self.speed_x = self.raw_speed_x * ratio
        self.speed_y = self.raw_speed_y * ratio
        
        # 图片
        if self.type == 1:
            if self.num == 1:
                self.rawimage = pygame.image.load("images/bullet1_supply.png").convert_alpha()
            elif self.num == 2:
                self.rawimage = pygame.image.load("images/bullet2_supply.png").convert_alpha()
            else:
                self.rawimage = pygame.image.load("images/bullet0_supply.png").convert_alpha()
        elif self.type == 2:
            self.rawimage = pygame.image.load("images/wingman_supply.png").convert_alpha()
        elif self.type == 3:
            self.rawimage = pygame.image.load("images/bomb_supply.png").convert_alpha()
        elif self.type == 4:
            self.rawimage = pygame.image.load("images/hp_supply.png").convert_alpha()
        elif self.type == 5:
            self.rawimage = pygame.image.load("images/sp_supply.png").convert_alpha()
        else:    #self.type == 0
            self.rawimage = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.raw_rect = self.rawimage.get_rect()
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        # 运动的部分
        self.degree = self.get_aim_degree()
        self.real_center_x += self.speed_x
        self.real_center_y += self.speed_y
        #显示的坐标
        self.rect.center = (int(self.real_center_x),int(self.real_center_y))
        
        # 改变速度的部分
        r_square = math.pow(self.real_center_x-self.aim[0],2) + \
                          math.pow(self.real_center_y-self.aim[1],2)
        if r_square > 100:
            gravity = 80/r_square
            ac_x = -gravity * math.cos(self.degree)
            if 0 < ac_x < 0.1:
                ac_x = 0.1
            elif -0.1 < ac_x < 0:
                ac_x = -0.1
            self.speed_x = self.speed_x + ac_x
            
            ac_y = -gravity * math.sin(self.degree)
            if 0 < ac_y < 0.1:
                ac_y = 0.1
            elif -0.1 < ac_y < 0:
                ac_y = -0.1
            self.speed_y = self.speed_y + ac_y
        else:
            ac_x,ac_y=0.0,0.0
        
        if self.die_timer > 0:
            self.die_timer -= 1
            if self.die_timer <= 60*3 and not self.flashing: 
                self.flashing = True
            if self.die_timer <= 0 and self.active:
                self.active = False
            
    def get_aim_degree(self):
        # 从右x轴开始，转向下y轴的夹角
        delta_x = self.real_center_x - self.aim[0]
        delta_y = self.real_center_y - self.aim[1]
        if delta_y == 0:
            if delta_x > 0:
                degree = 0
            else:
                degree = math.pi
        elif delta_y > 0:
            degree = -math.atan(delta_x/delta_y) + math.pi/2
        elif delta_y < 0:
            degree = -math.atan(delta_x/delta_y) - math.pi/2
        return degree
        
