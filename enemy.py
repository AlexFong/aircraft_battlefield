#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
from random import *
import math

class Enemy_1(pygame.sprite.Sprite):    # 继承
    def __init__(self,x,y,screen_size,ratio):    # speed=None,mode=None,move=None
        pygame.sprite.Sprite.__init__(self)
        
        self.active = True
        self.hp = 1
        self.die_timer = 0
        self.die_frame = 5
        self.ratio = ratio
        
        # 传入bg的参数做限制
        self.width = screen_size[0]
        self.height = screen_size[1]
        
        
        # 设定移动的方向和速度
        ## 移动的目标点，只是用于求初速度
        self.aim = (randint(int(screen_size[0]*4/10),int(screen_size[0]*6/10)),\
                    randint(int(screen_size[1]*4/10),int(screen_size[1]*6/10)))
        self.frame = randint(120,300)    # 移动至目标点需要的帧数
        self.raw_speed_x = int((self.aim[0] - x)/self.frame)
        self.raw_speed_y = int((self.aim[1] - y)/self.frame)
        self.speed_x = self.raw_speed_x * self.ratio
        self.speed_y = self.raw_speed_y * self.ratio
        
        # 旋转
        self.degree = get_enemy_1_degree(self.speed_x,self.speed_y)
        
        # 图片
        self.enemy1 = pygame.image.load("images/enemy1.png").convert_alpha()
        self.enemy1_down1 = pygame.image.load("images/enemy1_down1.png").convert_alpha()
        self.enemy1_down2 = pygame.image.load("images/enemy1_down2.png").convert_alpha()
        self.enemy1_down3 = pygame.image.load("images/enemy1_down3.png").convert_alpha()
        self.enemy1_down4 = pygame.image.load("images/enemy1_down4.png").convert_alpha()
        self.rawimage = self.enemy1
        self.raw_rect = self.rawimage.get_rect()
        
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        self.rect = self.image.get_rect()
        self.real_center_x = x
        self.real_center_y = y
        self.rect.center = (self.real_center_x,self.real_center_y)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.real_center_x = self.real_center_x + self.speed_x
        self.real_center_y = self.real_center_y + self.speed_y
        self.rect.center = (self.real_center_x,self.real_center_y)
        
    # 边界碰撞后处理
    def edge_collide(self):
        if self.rect.center[0] < -250 or \
        self.rect.center[0] > self.width + 250 or \
        self.rect.center[1] < -250 or \
        self.rect.center[1] > self.height +250:
            return True
        else:
            return False
    
    def get_hurt(self,hurt_num):
        if self.active:
            self.hp -= hurt_num
            if self.hp <= 0:
                self.active = False
        
    def check_die(self):
        if self.hp <= 0 and self.active == True:
            self.active = False
            
        if self.active == False:
            if self.die_timer/self.die_frame == 4:
                return True
            else:
                if self.die_timer/self.die_frame == 0:
                    self.image = self.enemy1_down1
                    self.image = pygame.transform.smoothscale(self.image,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
                    self.image = pygame.transform.rotate(self.image,self.degree)
                elif self.die_timer/self.die_frame == 1:
                    self.image = self.enemy1_down2
                    self.image = pygame.transform.smoothscale(self.image,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
                    self.image = pygame.transform.rotate(self.image,self.degree)
                elif self.die_timer/self.die_frame == 2:
                    self.image = self.enemy1_down3
                    self.image = pygame.transform.smoothscale(self.image,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
                    self.image = pygame.transform.rotate(self.image,self.degree)
                elif self.die_timer/self.die_frame == 3:
                    self.image = self.enemy1_down4
                    self.image = pygame.transform.smoothscale(self.image,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
                    self.image = pygame.transform.rotate(self.image,self.degree)
                self.die_timer += 1
                
                if self.die_timer == 1:
                    return 2
                else:
                    return False
        else:
            return False

# 获取enemy_1的夹角
def get_enemy_1_degree(speed_x,speed_y):    
    if speed_y == 0:
        if speed_x > 0:
            degree = 90
        else:
            degree = 270
    elif speed_y > 0:
        degree = math.atan(speed_x/speed_y)*180/math.pi
    elif speed_y < 0:
        degree = math.atan(speed_x/speed_y)*180/math.pi +180
    return degree
    