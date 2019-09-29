#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import math


class Myplane(pygame.sprite.Sprite):    # 继承
    def __init__(self,ratio,screen_size):
        pygame.sprite.Sprite.__init__(self)
        
        # [shoot_consume,bullet_power,bullet_speed,bullet_frequency]
        # [每次耗蓝，子弹威力，子弹速度，子弹射速]
        self.gun_type_dict = {0:{"shoot_consume":1/2,"bullet_power":1,"bullet_speed":25,"bullet_frequency":60/10},
                                 1:{"shoot_consume":1/2,"bullet_power":1,"bullet_speed":25,"bullet_frequency":60/10},
                                 2:{"shoot_consume":1/2,"bullet_power":1,"bullet_speed":25,"bullet_frequency":60/10}}
        
        self.hp_max = 10
        self.hp = 10    
        
        self.sp_max = 100
        self.sp = 100    
        self.sp_recover_rate = 2
        
        self.wingman = 0    # 僚机
        self.wingman_max = 2
        
        self.bomb_num = 3    
        self.bomb_num_max = 3
        # 0子弹数量，1子弹类型，2僚机，3大招，4血，5蓝
        
        self.gun_type = 0    
        self.gun_num = 1    
        self.gun_num_max = 5
        
        self.shoot_consume = self.gun_type_dict[self.gun_type]["shoot_consume"]    # 每一SP可以发2发
        #self.bullet_power = self.gun_type_dict[self.gun_type]["bullet_power"]
        #self.bullet_speed = self.gun_type_dict[self.gun_type]["bullet_speed"]
        self.bullet_frequency = self.gun_type_dict[self.gun_type]["bullet_frequency"]    # 每秒20发

        self.active = True
        self.die_timer = 0
        self.die_frame = 5
        
        self.hurting = False
        self.hurting_timer = 0
        self.hurting_frame = 120
        
        self.ratio = ratio
        self.degree = 0
        
        # 图片
        self.rawimage1 = pygame.image.load("images/me1.png").convert_alpha()
        self.rawimage2 = pygame.image.load("images/me2.png").convert_alpha()
        self.raw_rect = self.rawimage1.get_rect()
        
        # 做比例转换
        self.transform_image1 = pygame.transform.smoothscale(self.rawimage1,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.transform_image2 = pygame.transform.smoothscale(self.rawimage2,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        
        # 因为会不断对self.image旋转，所以需要方法的中间件
        self.chosen_image = self.transform_image1    # 不能删，很重要！！
        
        self.image = self.chosen_image    # 最后打印的是这个变量
        self.rect = self.image.get_rect()    # 最后打印的是这个rect
        
        self.real_center_x = screen_size[0]*0.5
        self.real_center_y = screen_size[1]*0.7
        self.rect.center = (self.real_center_x,self.real_center_y)
        
        
        # 传入bg的参数做限制,设定边界碰撞物
        self.width = screen_size[0]
        self.height = screen_size[1]
        
        # 阻力系数
        self.f = 0.08
        self.raw_acspeed = 60/60
        self.acspeed = self.raw_acspeed * self.ratio
        
        self.speed_x = 0
        self.speed_y = 0
        self.mask = pygame.mask.from_surface(self.image)
        
    def slowdown(self):
        self.speed_x = (1-self.f) * self.speed_x
        self.speed_y = (1-self.f) * self.speed_y
        if -0.02 < self.speed_x < 0.02:
            self.speed_x = 0
        if -0.02 < self.speed_y < 0.02:
            self.speed_y = 0
        
    def move_left(self):
        self.speed_x += -self.acspeed
    def move_right(self):
        self.speed_x += self.acspeed
    def move_up(self):
        self.speed_y += -self.acspeed
    def move_down(self):
        self.speed_y += self.acspeed
        
    def rotate(self):
        self.image = pygame.transform.rotate(self.chosen_image,self.degree)###########
        self.mask = pygame.mask.from_surface(self.image)    # 这里是应付改变分辨率的特殊处理
        self.rect = self.image.get_rect()    # 重新赋值
        
    def move(self):
        if self.speed_x or self.speed_y:
            self.real_center_x += self.speed_x
            self.real_center_y += self.speed_y
        self.rect.center = (int(self.real_center_x),int(self.real_center_y))
        
        
    # 边界碰撞后处理
    def edge_collide(self,direction):
        if direction == "left":
            self.speed_x = -self.speed_x  + 2
        elif direction == "right":
            self.speed_x = -self.speed_x  - 2
        elif direction == "top":
            self.speed_y = -self.speed_y  + 2
        elif direction == "bottom":
            self.speed_y = -self.speed_y  - 2
    
    
    # 每60帧恢复一次
    def get_sp(self):
        if self.sp < self.sp_max:
            self.sp += self.sp_recover_rate
            if self.sp > self.sp_max:
                self.sp = self.sp_max
                
    
        
    def get_hurt(self,hurt_num):
        if self.hurting == False and self.active:
            self.hp -= hurt_num
            if self.hp <= 0:
                self.active = False
            else:
                self.hurting = True
            return True    # return的值用来判断是否播音效
        else:
            return False
        
    def get_bonus(self,bonus_type,bonus_num):
        # 0子弹数量，1子弹类型，2僚机，3大招，4血，5蓝
        if bonus_type == 0 and self.gun_num < self.gun_num_max:
            self.gun_num += 1
        elif bonus_type == 1:
            if bonus_num not in [0,1,2]:
                self.gun_type = 0
            else:
                self.gun_type = bonus_num
        elif bonus_type == 2 and self.wingman < self.wingman_max:
            self.wingman += 1
        elif bonus_type == 3 and self.bomb_num < self.bomb_num_max: 
            self.bomb_num += 1
        elif bonus_type == 4:
            if bonus_num > 0:
                temp = bonus_num
            else:
                temp = 1
            self.hp = self.hp + temp
            if self.hp > self.hp_max:
                self.hp = self.hp_max
        elif bonus_type == 5:
            if bonus_num > 0:
                temp = bonus_num
            else:
                temp = 10
            self.sp = self.sp + temp
            if self.sp > self.sp_max:
                self.sp = self.sp_max
        
        
    def shoot(self):
        if self.sp > self.shoot_consume:
            self.sp -= self.shoot_consume
            return True
        else:
            return False
        
    def position(self,position):    # 对x做1个像素的偏移，修正中心点偏斜的问题    ##############因为这里调用太频繁？？################
        if position == "left_top":
            return [int(self.rect.center[0] + (-63+43)*math.sin((self.degree/180)*math.pi)\
                            +(-33)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (-63+43)*math.cos((self.degree/180)*math.pi)\
                            -(-33)*math.sin((self.degree/180)*math.pi))]
        elif position == "right_top":
            return [int(self.rect.center[0] + (-63+43)*math.sin((self.degree/180)*math.pi)\
                            +(33)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (-63+43)*math.cos((self.degree/180)*math.pi)\
                            -(33)*math.sin((self.degree/180)*math.pi))]
        elif position == "top":    
            return [int(self.rect.center[0] + (-63)*math.sin((self.degree/180)*math.pi)\
                            +(1)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (-63)*math.cos((self.degree/180)*math.pi)\
                           -(1)*math.sin((self.degree/180)*math.pi))]
        elif position == "top_left":
            return [int(self.rect.center[0] + (-60)*math.sin((self.degree/180)*math.pi)\
                            +(-5+1)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (-60)*math.cos((self.degree/180)*math.pi)\
                            -(-5+1)*math.sin((self.degree/180)*math.pi))]
        elif position == "top_right":
            return [int(self.rect.center[0] + (-60)*math.sin((self.degree/180)*math.pi)\
                            +(5+1)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (-60)*math.cos((self.degree/180)*math.pi)\
                            -(5+1)*math.sin((self.degree/180)*math.pi))]
        elif position == "bottom":
            return [int(self.rect.center[0] + (+63-30)*math.sin((self.degree/180)*math.pi)\
                            +(1)*math.cos((self.degree/180)*math.pi)),\
                    int(self.rect.center[1] + (+63-30)*math.cos((self.degree/180)*math.pi)\
                            -(1)*math.sin((self.degree/180)*math.pi))]
        
            
    def gen_bullet(self):
        #Myplane_bullet(me.rect.center[0],me.rect.center[1],get_me_degree(),me.bullet_power,me.bullet_speed,screen_size)
        bullet_list = []
        # 这里要解决的是挂点和角度的问题
        if self.gun_type == 0 or 1 or 2:
            if self.gun_num == 1:
                bullet_list.append([self.position("top"),self.degree])
            elif self.gun_num == 2:
                bullet_list.append([self.position("top_left"),self.degree])
                bullet_list.append([self.position("top_right"),self.degree])
            elif self.gun_num == 3:
                bullet_list.append([self.position("top"),self.degree])
                bullet_list.append([self.position("left_top"),self.degree])
                bullet_list.append([self.position("right_top"),self.degree])
            elif self.gun_num == 4:
                bullet_list.append([self.position("left_top"),self.degree])
                bullet_list.append([self.position("right_top"),self.degree])
                bullet_list.append([self.position("top_left"),self.degree])
                bullet_list.append([self.position("top_right"),self.degree])
            elif self.gun_num == 5:
                bullet_list.append([self.position("top"),self.degree])
                bullet_list.append([self.position("left_top"),self.degree])
                bullet_list.append([self.position("right_top"),self.degree])
                bullet_list.append([self.position("top_left"),self.degree])
                bullet_list.append([self.position("top_right"),self.degree])

            
        #if self.gun_type == 1:
            
            
        #if self.gun_type == 2:
        return bullet_list
        
        
class Weiqi(pygame.sprite.Sprite):    #继承
    def __init__(self,ratio,me_center_x,me_center_y,degree):
        pygame.sprite.Sprite.__init__(self)
        
        self.ratio = ratio
        self.degree = degree
        
        self.rawimage = pygame.image.load("images/weiqi.png").convert_alpha()
        self.raw_rect = self.rawimage.get_rect()
        # 做比例转换
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        self.rect = self.image.get_rect()
        self.rect.center = \
            (me_center_x + (63-10)*self.ratio*math.sin(degree/180*math.pi),\
            me_center_y + (63-10)*self.ratio*math.cos(degree/180*math.pi))


class Myplane_bullet(pygame.sprite.Sprite):    #继承
    def __init__(self,gun_type,gun_type_dict,position_degree,screen_size,ratio):
        pygame.sprite.Sprite.__init__(self)
        
        # 把不同类型的飞机数据储存在字典列表中
        # [shoot_consume,bullet_power,bullet_speed,bullet_frequency]
        # [每次耗蓝，子弹威力，子弹速度，子弹射速]
        self.power = gun_type_dict[gun_type]["bullet_power"]
        self.speed = gun_type_dict[gun_type]["bullet_speed"]
        
        self.degree = position_degree[1]
        
        self.width = screen_size[0]
        self.height = screen_size[1]
        
        # convert_alpha()后不能用一般方法设置透明
        if gun_type == 0:
            self.rawimage = pygame.image.load("images/bullet1.png").convert_alpha()    # 小橙
        if gun_type == 1:
            self.rawimage = pygame.image.load("images/bullet4.png").convert_alpha()    # 大蓝
            #self.rawimage = pygame.image.load("images/bullet2.png").convert_alpha()    # 小蓝
        if gun_type == 2:
            self.rawimage = pygame.image.load("images/bullet5.png").convert_alpha()    # 中紫
            #self.rawimage = pygame.image.load("images/bullet3.png").convert_alpha()    # 小红
        
        self.raw_rect = self.rawimage.get_rect()
        self.ratio = ratio    ####################################################改分辨率判断要部署的####################
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        self.rect = self.image.get_rect()
        self.rect.center = position_degree[0]    ######################
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.rect.center = (self.rect.center[0] - self.speed*math.sin(self.degree/180*math.pi),\
                           self.rect.center[1] - self.speed*math.cos(self.degree/180*math.pi))
        #self.mask = pygame.mask.from_surface(self.image)
        
    def edge_collide(self):
        if self.rect.center[0] < -10 or \
        self.rect.center[0] > self.width + 10 or \
        self.rect.center[1] < -10 or \
        self.rect.center[1] > self.height +10:
            return True
        else:
            return False
        
        
        