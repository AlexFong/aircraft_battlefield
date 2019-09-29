import pygame
import sys
import os
os.chdir(sys.argv[0][0:sys.argv[0].rfind("/")])    # 把目录设置为当前文件所在目录
import traceback
import math
from pygame.locals import *
from interval import Interval
from random import *

from myplane import *
from edge import *
from enemy import *
from bonus import *
from button import *


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


# 参数定义6666666666666666666666666
screen_size_default = width,height = 1600,900#1600,900
fullscreen_size = width,height = 1920,1080
screen_size = screen_size_default
# 缩放比,原来的坐标是逻辑坐标，缩放后的坐标是渲染的坐标
ratio = screen_size[1]/screen_size_default[1]


screen = pygame.display.set_mode(screen_size,HWSURFACE)
pygame.display.set_caption("飞机大战")
screen2 = screen.convert_alpha()    # screen2是透明度图层


# 分辨率设置
screen_size_list = pygame.display.list_modes()
screen_size_setting = Setting_drawer(ratio,value=screen_size,list=screen_size_list,\
                    text="分辨率",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2,screen_size[1]*0.39),\
                    size=(screen_size_default[0]/2,50),color=(50,50,50,150))
setting_drawer_group = pygame.sprite.Group()
setting_drawer_group.add(screen_size_setting)

screen_mode_default = "窗口化"    #初始化全屏设置
#screen_mode_dict = {"窗口化":None,"全屏":"FULLSCREEN"}
screen_mode_key_list = ["窗口化","全屏"]
screen_mode_value_list = [None,"FULLSCREEN"]
screen_mode = Setting_choice(ratio,key=screen_mode_default,\
                list1=screen_mode_key_list,list2=screen_mode_value_list,\
                text="显示模式",text_size=24,text_color=(255,255,255),\
                center=(screen_size_default[0]/2,screen_size[1]*0.45),\
                size=(screen_size_default[0]/2,50),color=(50,50,50,150))
setting_choice_group = pygame.sprite.Group()
setting_choice_group.add(screen_mode)


frequancy = 60
loop = 0

# 界面开关
homepage = True
homepage_setting = False
homepage_ranking = False

gamepage = False
gamepage_paused = False
gamepage_paused_setting = False

diepage = False


# UI按键开关
pause_button_active = False    # 这个图片开关没法生成类对象，特殊处理

# 按住按键时，可不断调用按键，（第一次发送事件的延迟时间ms，制定重复发送的时间间隔）
#pygame.key.set_repeat(int(1000/frequancy),int(1000/frequancy))

# 初始化mouse_pos属性，让飞机一开始指向上
mouse_pos = (screen_size[0]/2,screen_size[1]/2)

# 功能开关
switch_up = False
switch_down = False
switch_left = False
switch_right = False
switch_mouse_left = False
switch_shoot = False
shoot_ready = True
loop_shoot_ready = False
#loop_gen_bullet = False
loop_gen_bullet1 = False
loop_gen_bullet2 = False
bullet_sound_delay = 6

clock = pygame.time.Clock()


# 日志
#screen_size_logger = []
temp_screen_size = screen_size


#导入区2222222222222222222222222222222222222222
## 图片
bg = pygame.image.load("bgimages/bg.jpg")
resume_nor = pygame.image.load("images/resume_nor.png").convert_alpha()
resume_pressed = pygame.image.load("images/resume_pressed.png").convert_alpha()
pause_nor = pygame.image.load("images/pause_nor.png").convert_alpha()
pause_pressed = pygame.image.load("images/pause_pressed.png").convert_alpha()
pause_button = pause_nor



## 文字
def font_fs(size):
    return pygame.font.Font("font/BrushScriptStd.ttf",size)    # 仿宋的感觉
def font_kt(size):
    return pygame.font.Font("font/font.ttf",size)    # 卡通
def font_msyh(size):
    return pygame.font.Font("font/msyh.ttf",size)    # 微软雅黑 




# 创建类对象5555555555555555
me = Myplane(ratio,screen_size)


## UI对象
start_button = Button(ratio,\
        center=(screen_size[0]*0.5,screen_size[1]*0.3),size=(500,100),text=" 飞机大战!")
setting_button = Button(ratio,\
        center=(screen_size[0]*0.5,screen_size[1]*0.45),size=(500,100),text=" 设置")
ranking_button = Button(ratio,\
        center=(screen_size[0]*0.5,screen_size[1]*0.6),size=(500,100),text=" 排行榜")
exit_button = Button(ratio,\
        center=(screen_size[0]*0.5,screen_size[1]*0.75),size=(500,100),text=" 退出游戏")

button_group = pygame.sprite.Group()
button_group.add(start_button)
button_group.add(setting_button)
button_group.add(ranking_button)
button_group.add(exit_button)


# 音量设置
total_volume_default = 0.5
effect_volume_default = 0.2
bgm_volume_default = 0.1

total_volume = Setting_touch_bar(ratio,value=total_volume_default,text="总音量",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2,screen_size[1]*0.2),size=(800,50),color=(50,50,50,150))
effect_volume = Setting_touch_bar(ratio,value=effect_volume_default,text="音效音量",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2+25,screen_size[1]*0.26),size=(750,50),color=(50,50,50,150))
bgm_volume = Setting_touch_bar(ratio,value=bgm_volume_default,text="背景音量",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2+25,screen_size[1]*0.32),size=(750,50),color=(50,50,50,150))
setting_touch_bar_group = pygame.sprite.Group()
setting_touch_bar_group.add(total_volume)
setting_touch_bar_group.add(effect_volume)
setting_touch_bar_group.add(bgm_volume)


## bgm
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(total_volume.value*bgm_volume.value)    #0-1
pygame.mixer.music.play()


## 音效
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")    # 瞬间的音效要让画面做delay，不然不跟手
bullet_sound.set_volume(total_volume.value*effect_volume.value)
button_sound = pygame.mixer.Sound("sound/button.wav")
button_sound.set_volume(total_volume.value*effect_volume.value)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(total_volume.value*effect_volume.value)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(total_volume.value*effect_volume.value)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(total_volume.value*effect_volume.value)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(total_volume.value*effect_volume.value)
get_supply_sound = pygame.mixer.Sound("sound/supply.wav")
get_supply_sound.set_volume(total_volume.value*effect_volume.value)
get_upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
get_upgrade_sound.set_volume(total_volume.value*effect_volume.value)
# 未处理
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(total_volume.value*effect_volume.value)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(total_volume.value*effect_volume.value)
enemy3_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(total_volume.value*effect_volume.value)
use_bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
use_bomb_sound.set_volume(total_volume.value*effect_volume.value)

def set_effect_volume():
    bullet_sound.set_volume(total_volume.value*effect_volume.value)
    button_sound.set_volume(total_volume.value*effect_volume.value)
    enemy1_down_sound.set_volume(total_volume.value*effect_volume.value)
    me_down_sound.set_volume(total_volume.value*effect_volume.value)
    get_bomb_sound.set_volume(total_volume.value*effect_volume.value)
    get_bullet_sound.set_volume(total_volume.value*effect_volume.value)
    get_supply_sound.set_volume(total_volume.value*effect_volume.value)
    get_upgrade_sound.set_volume(total_volume.value*effect_volume.value)
    # 未处理
    enemy2_down_sound.set_volume(total_volume.value*effect_volume.value)
    enemy3_down_sound.set_volume(total_volume.value*effect_volume.value)
    enemy3_flying_sound.set_volume(total_volume.value*effect_volume.value)
    use_bomb_sound.set_volume(total_volume.value*effect_volume.value)



## 创建精灵组
weiqi_group = pygame.sprite.Group()

myplane_bullet_group = pygame.sprite.Group()

enemy_1_num = 10    # 会有其他进程控制这个数量
enemy_1_group = pygame.sprite.Group()

bonus_group = pygame.sprite.Group()

edge_group = pygame.sprite.Group()
edge_group.add(Edge("left",0-100,0-100,100,screen_size[1]+200))
edge_group.add(Edge("top",0-100,0-100,screen_size[0]+200,100))
edge_group.add(Edge("right",screen_size[0],0-100,100,screen_size[1]+200))
edge_group.add(Edge("bottom",0-100,screen_size[1],screen_size[0]+200,100))


#方法定义#################################################
# 特殊的设置图片透明度方法，通过创建一个copy
def set_image_alpha(each,screen,alpha_num):
    location = each.rect
    x = location[0]
    y = location[1]
    temp = pygame.Surface((each.image.get_width(),\
                        each.image.get_height())).convert()
    temp.blit(screen,(-x,-y))
    temp.blit(each.image,(0,0))
    temp.set_alpha(alpha_num)
    screen.blit(temp,location)


def pause():
    global gamepage_paused,gamepage
    gamepage_paused = not gamepage_paused
    #gamepage = not gamepage
    if gamepage_paused:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

        

# 获取鼠标与飞机的夹角
def get_me_degree():
    delta_x = mouse_pos[0] - me.real_center_x
    delta_y = mouse_pos[1] - me.real_center_y
    if delta_x == 0 and delta_y == 0:
        pass
    elif delta_x == 0:
        if delta_y > 0:
            me_degree = 180
        if delta_y < 0:
            me_degree = 0    
    elif delta_y == 0:
        if delta_x > 0:
            me_degree = 270
        else:
            me_degree = 90
    elif delta_y > 0:
        me_degree = math.atan(delta_x/delta_y)*180/math.pi +180
    elif delta_y < 0:
        me_degree = math.atan(delta_x/delta_y)*180/math.pi
    me.degree = me_degree


def get_enemy_born_position(area=None):
    if area == None:    
        position = (randint(-200,screen_size[0]+200),randint(-200,screen_size[1]+200))
        while position[0] in Interval(-50,screen_size[0]+50) or \
                position[1] in Interval(-50,screen_size[1]+50):
            position = (randint(-200,screen_size[0]+200),randint(-200,screen_size[1]+200))
    # 完善功能
    return position


def get_bonus_born_position(): 
    position = (randint(0,screen_size[0]),randint(0,screen_size[1]))
    while position[0] in Interval(screen_size[0]*0.3,screen_size[0]*0.7) or \
            position[1] in Interval(screen_size[1]*0.3,screen_size[1]*0.7):
        position = (randint(0,screen_size[0]),randint(0,screen_size[1]))
    return position


def screen_change(ratio,screen_size,change_screen_size):############################################################
    def position_change_x(x):
        return change_screen_size[0]/2 + (x - screen_size[0]/2) * pos_ratio
    def position_change_y(y):
        return change_screen_size[1]/2 + (y - screen_size[1]/2) * pos_ratio

    pos_ratio = change_screen_size[1] / screen_size[1]
    
    
    # 凡是涉及ratio的参数都要做一个raw备份
    me.ratio = ratio
    me.width = change_screen_size[0]
    me.height = change_screen_size[1]
    me.transform_image1 = pygame.transform.smoothscale(me.rawimage1,\
                     (int(me.raw_rect.width*me.ratio),int(me.raw_rect.height*me.ratio)))
    me.transform_image2 = pygame.transform.smoothscale(me.rawimage2,\
                     (int(me.raw_rect.width*me.ratio),int(me.raw_rect.height*me.ratio)))
    me.real_center_x = position_change_x(me.real_center_x)
    me.real_center_y = position_change_y(me.real_center_y)
    me.acspeed = me.raw_acspeed * me.ratio
    
    
    for each in button_group:
        each.ratio = ratio
        each.center = (int(position_change_x(each.center[0])),\
                               int(position_change_y(each.center[1])))
        each.size = (int(each.raw_size[0]*ratio),\
                             int(each.raw_size[1]*ratio))
        each.rect = (int(each.center[0]-each.size[0]*0.5),\
                             int(each.center[1]-each.size[1]*0.5),\
                             each.size[0],each.size[1])
        each.text_size = int(each.raw_text_size*ratio)
        each.font = pygame.font.Font("font/msyh.ttf",each.text_size)
    
    
    for self in weiqi_group:    # 这里用self替代each是为了偷懒
        self.ratio = ratio
        # 做比例转换
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        temp_center = (int(position_change_x(self.rect.center[0])),\
                            int(position_change_y(self.rect.center[1])))
        self.rect = self.image.get_rect()
        self.rect.center = temp_center
    
    
    for self in myplane_bullet_group:    # 这里执行顺序有优化空间
        self.ratio = ratio    ################################################改分辨率判断要部署的####################
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        temp_center = (int(position_change_x(self.rect.center[0])),\
                            int(position_change_y(self.rect.center[1])))
        self.rect = self.image.get_rect()
        self.rect.center = temp_center    
        self.mask = pygame.mask.from_surface(self.image)######################
        
    
    for self in enemy_1_group:
        self.ratio = ratio
        self.width = change_screen_size[0]
        self.height = change_screen_size[1]
        self.speed_x = self.raw_speed_x * self.ratio
        self.speed_y = self.raw_speed_y * self.ratio
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        temp_center = (int(position_change_x(self.rect.center[0])),\
                            int(position_change_y(self.rect.center[1])))
        self.rect = self.image.get_rect()
        self.rect.center = temp_center
        self.mask = pygame.mask.from_surface(self.image)
        
        
    for self in bonus_group:
        self.ratio = ratio
        self.width = change_screen_size[0]
        self.height = change_screen_size[1]
        self.aim = (position_change_x(self.aim[0]),position_change_y(self.aim[1]))
        self.real_center_x = position_change_x(self.real_center_x)
        self.real_center_y = position_change_y(self.real_center_y)
        self.speed_x = self.raw_speed_x * self.ratio
        self.speed_y = self.raw_speed_y * self.ratio
        self.transform_image = pygame.transform.smoothscale(self.rawimage,\
                 (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.image = pygame.transform.rotate(self.transform_image,self.degree)
        temp_center = (int(position_change_x(self.rect.center[0])),\
                            int(position_change_y(self.rect.center[1])))
        self.rect = self.image.get_rect()
        self.rect.center = temp_center
        self.mask = pygame.mask.from_surface(self.image)
    
    
    edge_group.empty()
    edge_group.add(Edge("left",0-100,0-100,100,change_screen_size[1]+200))
    edge_group.add(Edge("top",0-100,0-100,change_screen_size[0]+200,100))
    edge_group.add(Edge("right",change_screen_size[0],0-100,100,change_screen_size[1]+200))
    edge_group.add(Edge("bottom",0-100,change_screen_size[1],change_screen_size[0]+200,100))
    
    
    for self in setting_drawer_group:
        self.ratio = ratio
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.center = (position_change_x(self.center[0]),\
                        position_change_y(self.center[1]))
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)
        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                        int(self.center[1]-self.size[1]*0.5),\
                        self.size[0],\
                        self.size[1])
        self.list_per_height = self.raw_list_per_height * self.ratio
        self.top_rect = (position_change_x(self.top_rect[0]),\
                        position_change_y(self.top_rect[1]),\
                        screen_size_default[0]*0.16*self.ratio,\
                        self.list_per_height)
        self.list_rect = (position_change_x(self.list_rect[0]),\
                        position_change_y(self.list_rect[1]),\
                        screen_size_default[0]*0.16*self.ratio,\
                        self.list_num*self.list_per_height)
        self.bar_height = self.list_per_height*10*10/len(self.list)


    for self in setting_touch_bar_group:
        self.ratio = ratio
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.center = (position_change_x(self.center[0]),\
                        position_change_y(self.center[1]))
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)
        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                        int(self.center[1]-self.size[1]*0.5),\
                        self.size[0],\
                        self.size[1])
        self.bar_empty_rect = (position_change_x(self.bar_empty_rect[0]), \
                                position_change_y(self.bar_empty_rect[1]),\
                                screen_size_default[0]*0.12*self.ratio, \
                                self.rect[3]*0.2)
        self.bar_fill_rect = (position_change_x(self.bar_fill_rect[0]), \
                                position_change_y(self.bar_fill_rect[1]),\
                                screen_size_default[0]*0.12*self.ratio*self.value, \
                                self.rect[3]*0.2)
        self.fill_point = int(self.bar_fill_rect[0]+self.bar_fill_rect[2]),\
                        int(self.bar_fill_rect[1]+self.bar_fill_rect[3]*0.5)
        self.num_position = (position_change_x(self.num_position[0]),\
                            position_change_y(self.num_position[1]))

    for self in setting_choice_group:
        self.ratio = ratio
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.center = (position_change_x(self.center[0]),\
                        position_change_y(self.center[1]))
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)
        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                        int(self.center[1]-self.size[1]*0.5),\
                        self.size[0],\
                        self.size[1])
        temp = (position_change_x(self.right_image_rect.center[0]),\
                position_change_y(self.right_image_rect.center[1]))
        self.right_image = pygame.transform.smoothscale(self.rawimage,\
                            (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.right_image_rect = self.right_image.get_rect()
        self.right_image_rect.center = temp
        temp = (position_change_x(self.left_image_rect.center[0]),\
                position_change_y(self.left_image_rect.center[1]))
        self.left_image = pygame.transform.rotate(self.right_image,180)
        self.left_image_rect = self.left_image.get_rect()
        self.left_image_rect.center = temp
        self.key_position = (position_change_x(self.key_position[0]),\
                                position_change_y(self.key_position[1]))


def pygame_event():
    global mouse_pos,switch_mouse_left,switch_shoot,switch_up,switch_down,switch_left,switch_right,\
            fullscreen,screen_size,temp_screen_size,\
            pause_button_active,\
            gamepage,gamepage_paused,gamepage_paused_setting,\
            homepage,homepage_ranking,homepage_setting,\
            diepage,ratio
            
            
    
    for event in pygame.event.get():
        # 全场景通用的
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if homepage:
                    if homepage_setting:
                        if screen_size_setting.active:
                            if screen_size_setting.on_bar(mouse_pos):
                                screen_size_setting.change_bar(mouse_pos)
                            elif screen_size_setting.on_list(mouse_pos):
                                button_sound.play()
                                print("screen_size_setting.on_list")
                                screen_size_setting.value = screen_size_setting.list[screen_size_setting.on_list(mouse_pos)-1]
                                # 因为0等价False，所以移了一位
                                change_screen_size = screen_size_setting.value
                                ratio = change_screen_size[1]/screen_size_default[1]
                                screen_change(ratio,screen_size,change_screen_size)    # 用于设配各对象
                                screen_size = change_screen_size
                                if screen_mode.value:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                                else:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE)
                                screen_size_setting.active = False
                            else:
                                screen_size_setting.active = False
                        else:
                            if total_volume.on_button(mouse_pos):
                                total_volume.active = True
                                button_sound.play()
                            elif effect_volume.on_button(mouse_pos):
                                effect_volume.active = True
                                button_sound.play()
                            elif bgm_volume.on_button(mouse_pos):
                                bgm_volume.active = True
                                button_sound.play()
                            elif screen_size_setting.on_button(mouse_pos):
                                button_sound.play()
                                screen_size_setting.active = not screen_size_setting.active
                            elif screen_mode.on_button_left(mouse_pos):
                                button_sound.play()
                                screen_mode.change(-1)
                                if screen_mode.value:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                                else:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE)
                            elif screen_mode.on_button_right(mouse_pos):
                                button_sound.play()
                                screen_mode.change(+1)
                                if screen_mode.value:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                                else:
                                    screen = pygame.display.set_mode(screen_size,HWSURFACE)
                    else:
                        if start_button.on_button(mouse_pos):
                            start_button.active = True
                            button_sound.play()
                        elif setting_button.on_button(mouse_pos):
                            setting_button.active = True
                            button_sound.play()
                        elif ranking_button.on_button(mouse_pos):
                            ranking_button.active = True
                            button_sound.play()
                        elif exit_button.on_button(mouse_pos):
                            exit_button.active = True
                            button_sound.play()

                elif gamepage and me.active:
                    if gamepage_paused:
                        if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                                mouse_pos[1] in range(30,70):
                            pause_button_active = True
                            button_sound.play()
                    
                    # 暂停按键判断
                    else:
                        if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                                mouse_pos[1] in range(30,70):
                            pause_button_active = True
                            button_sound.play()
                        else:
                            switch_shoot = True
                switch_mouse_left = True

            elif event.button == 4:
                if homepage:
                    if homepage_setting:
                        if screen_size_setting.active:
                            if screen_size_setting.on_bar(mouse_pos) or \
                                screen_size_setting.on_list(mouse_pos):
                                if screen_size_setting.list_head_index > 0:
                                    screen_size_setting.list_head_index -= 1
            elif event.button == 5:
                if homepage:
                    if homepage_setting:
                        if screen_size_setting.active:
                            if screen_size_setting.on_bar(mouse_pos) or \
                                screen_size_setting.on_list(mouse_pos):
                                if screen_size_setting.list_head_index + \
                                    screen_size_setting.list_num < len(screen_size_setting.list):
                                    screen_size_setting.list_head_index += 1
                    
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if homepage:
                    if homepage_setting:
                        total_volume.active = False
                        effect_volume.active = False
                        bgm_volume.active = False
                    else:
                        if start_button.on_button(mouse_pos) and start_button.active:
                            homepage = False
                            gamepage = True
                        elif setting_button.on_button(mouse_pos) and setting_button.active:
                            homepage_setting = True
                            homepage = True
                        elif ranking_button.on_button(mouse_pos) and ranking_button.active:
                            homepage_ranking = True
                            homepage = True
                        elif exit_button.on_button(mouse_pos) and exit_button.active:
                            pygame.quit()
                            sys.exit()
                        start_button.active = False
                        setting_button.active = False
                        ranking_button.active = False
                        exit_button.active = False
                
                elif gamepage and me.active:
                    if gamepage_paused:
                        # 松键判断
                        if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                                mouse_pos[1] in range(30,70) and pause_button_active:
                                # pause_button_active妙，不会引起在这松手继续射击的bug
                            pause()
                    else:
                        # 松键判断
                        if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                                mouse_pos[1] in range(30,70) and pause_button_active:
                                # pause_button_active妙，不会引起在这松手继续射击的bug
                            pause()
                        else:
                            switch_shoot = False
                        pause_button_active = False
                switch_mouse_left = False

        # KEYUP
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                switch_up = False
            if event.key == K_DOWN or event.key == K_s:
                switch_down = False
            if event.key == K_LEFT or event.key == K_a:
                switch_left = False
            if event.key == K_RIGHT or event.key == K_d:
                switch_right = False

        # KEYDOWN
        if event.type == KEYDOWN:    # 这种方法一次只能捕获一个按键???怎么突然又可以多键了。。。
            if gamepage:
                if event.key == K_ESCAPE:
                    pause()
                    button_sound.play()
            if event.key == K_UP or event.key == K_w:
                switch_up = True
            if event.key == K_DOWN or event.key == K_s:
                switch_down = True
            if event.key ==K_LEFT or event.key == K_a:
                switch_left = True
            if event.key == K_RIGHT or event.key == K_d:
                switch_right = True
            if event.key == K_z:
                print("zzz断点断点断点断点断点断点断点断点断点断点断点")
                change_screen_size = [randint(1200,1600),randint(600,1200)]#randint(600,1200)
                ratio = change_screen_size[1]/screen_size_default[1]
                screen_change(ratio,screen_size,change_screen_size)    # 用于设配各对象
                screen_size = change_screen_size
                if screen_mode.value:
                    screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(screen_size,HWSURFACE)
                
            if event.key == K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    #temp_screen_size = screen_size
                    change_screen_size = fullscreen_size
                    ratio = change_screen_size[1]/screen_size_default[1]
                    screen_change(ratio,screen_size,change_screen_size)    # 用于设配各对象
                    screen_size = change_screen_size
                    if screen_mode.value:
                        screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(screen_size,HWSURFACE)
                else:
                    change_screen_size = temp_screen_size
                    ratio = change_screen_size[1]/screen_size_default[1]
                    screen_change(ratio,screen_size,change_screen_size)    # 用于设配各对象
                    screen_size = change_screen_size
                    if screen_mode.value:
                        screen = pygame.display.set_mode(screen_size,HWSURFACE | FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(screen_size,HWSURFACE)
        


################################主循环#################################


while True:    # 游戏界面
    # 画布区
    #screen.blit(bg,(0,0))
    #screen.fill((255,255,255))
    screen2.fill((255,255,255,0))#alpha=0,全透明

    pygame_event()
    
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    
    if homepage:    #游戏主界面
        screen.blit(bg,(0,0))

        if homepage_setting:
            # 分辨率设置的功能
            screen_mode.draw(screen2)
            screen_size_setting.draw_top(screen2)
            if screen_size_setting.active:
                screen_size_setting.draw_list(screen2)

            # 音量设置
            if total_volume.active:
                total_volume.change(mouse_pos)
                pygame.mixer.music.set_volume(total_volume.value*bgm_volume.value)
                set_effect_volume()
            elif effect_volume.active:
                effect_volume.change(mouse_pos)
                pygame.mixer.music.set_volume(total_volume.value*bgm_volume.value)
                set_effect_volume()
            elif bgm_volume.active:
                bgm_volume.change(mouse_pos)
                pygame.mixer.music.set_volume(total_volume.value*bgm_volume.value)
                
            total_volume.draw(screen2)
            effect_volume.draw(screen2)
            bgm_volume.draw(screen2)

        elif homepage_ranking:
            pass
        else:
            if start_button.active and switch_mouse_left:
                start_button.color = start_button.color2
            else:
                start_button.color = start_button.color1
            start_button.draw(screen)

            if setting_button.active and switch_mouse_left:
                setting_button.color = setting_button.color2
            else:
                setting_button.color = setting_button.color1
            setting_button.draw(screen)

            if ranking_button.active and switch_mouse_left:
                ranking_button.color = ranking_button.color2
            else:
                ranking_button.color = ranking_button.color1
            ranking_button.draw(screen)

            if exit_button.active and switch_mouse_left:
                exit_button.color = exit_button.color2
            else:
                exit_button.color = exit_button.color1
            exit_button.draw(screen)


    elif diepage:
        pass
    
    elif gamepage:
        screen.fill((255,255,255))

        if gamepage_paused:    # 暂停界面
            if gamepage_paused_setting:    # 暂停设置界面
                pass
            else:    # 暂停界面
                if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                                mouse_pos[1] in range(30,70) and switch_mouse_left:
                    pause_button = resume_pressed
                else:
                    pause_button = resume_nor 
                screen.blit(pause_button,(screen_size[0]-65-20,30))    # 暂停按钮

        else:    # 游戏主循环界面
            
            # loop in Interval(1,60)
            loop += 1
            if loop == frequancy + 1:
                loop = 1

            
            # 处理移动事件#####################################################

            # me的部分
            me.slowdown()

            if switch_up:
                me.move_up()
            if switch_down:
                me.move_down()
            if switch_left:
                me.move_left()
            if switch_right:
                me.move_right()

            me_image_frequency = 5
            if loop%me_image_frequency == 0 and loop/me_image_frequency%2 == 0:
                me.chosen_image = me.transform_image2
            elif loop%me_image_frequency == 0 and loop/me_image_frequency%2 == 1:
                me.chosen_image = me.transform_image1

            get_me_degree()
            me.rotate()
            me.move()


            edge_collide_result = pygame.sprite.spritecollide(me,\
                                edge_group,False,pygame.sprite.collide_mask)
            if edge_collide_result:
                for each in edge_collide_result:    # 此处是碰撞的边界的集合
                    me.edge_collide(each.direction)

            if me.hurting == True:
                if me.hurting_timer < me.hurting_frame:
                    me.hurting_timer += 1
                elif me.hurting_timer >= me.hurting_frame:
                    me.hurting = False
                    me.hurting_timer = 0

            if loop == frequancy:
                me.get_sp()


            # 生成me的bullet,声音不跟手，先播声音，后生成子弹
            if loop == loop_shoot_ready:
                shoot_ready = True
                loop_shoot_ready = False
            if switch_shoot and me.active and shoot_ready:
                if me.shoot():    # 耗蓝方法
                    bullet_sound.play()
                    # 1个loop_gen_bullet只能延迟1个bullet_frequency，所以此处用了两个
                    if not loop_gen_bullet1 and not loop_gen_bullet2:
                        loop_gen_bullet1 = loop + bullet_sound_delay    # 用这个参数处理延迟手感
                        if loop_gen_bullet1 > frequancy:
                            loop_gen_bullet1 = loop_gen_bullet1 - frequancy
                    elif loop_gen_bullet1 and not loop_gen_bullet2:
                        loop_gen_bullet2 = loop + bullet_sound_delay
                        if loop_gen_bullet2 > frequancy:
                            loop_gen_bullet2 = loop_gen_bullet2 - frequancy
                    elif not loop_gen_bullet1 and loop_gen_bullet2:
                        loop_gen_bullet1 = loop + bullet_sound_delay
                        if loop_gen_bullet1 > frequancy:
                            loop_gen_bullet1 = loop_gen_bullet1 - frequancy

                    loop_shoot_ready = loop + me.gun_type_dict[me.gun_type]["bullet_frequency"]
                    if loop_shoot_ready > frequancy:
                        loop_shoot_ready = loop_shoot_ready - frequancy
                    shoot_ready = False
            if loop == loop_gen_bullet1:
                bullet_list = me.gen_bullet()    # 这里不够完美，但是忽略
                for each in bullet_list:
                    myplane_bullet_group.add(Myplane_bullet\
                                (me.gun_type,me.gun_type_dict,each,screen_size,ratio))
                loop_gen_bullet1 = False
            elif loop == loop_gen_bullet2:
                bullet_list = me.gen_bullet()    # 这里不够完美，但是忽略
                for each in bullet_list:
                    myplane_bullet_group.add(Myplane_bullet\
                                (me.gun_type,me.gun_type_dict,each,screen_size,ratio))
                loop_gen_bullet2 = False


            for each in myplane_bullet_group:    # 优化时可以跟其他循环合并
                each.move()
                if each.edge_collide():
                    myplane_bullet_group.remove(each)
                    #continue


            # 尾气部分
            weiqi_num = frequancy - 50
            weiqi_obj = Weiqi(ratio,me.real_center_x,me.real_center_y,me.degree)
            weiqi_group.add(weiqi_obj)
            if len(weiqi_group) == weiqi_num + 1:
                for each in weiqi_group:
                    weiqi_group.remove(each)
                    break


            # enemy_1
            ## 生成
            #if loop == frequancy and len(enemy_1_group) < enemy_1_num:
            if frequancy%loop and len(enemy_1_group) < enemy_1_num:
                position = get_enemy_born_position()
                enemy_1_group.add(Enemy_1(position[0],position[1],screen_size,ratio))


            # 改变状态后的事件判断##################################################


            ## enemy_1与me碰撞
            enemy_1_me_collide = pygame.sprite.spritecollide(me,\
                                enemy_1_group,False,pygame.sprite.collide_mask)
            if enemy_1_me_collide:
                if me.get_hurt(1):
                    me_down_sound.play()
                for each in enemy_1_me_collide:
                    each.get_hurt(1)


            ## 与myplane_bullet碰撞
            enemy_1_myplane_bullet_collide = pygame.sprite.groupcollide(enemy_1_group,\
                                myplane_bullet_group,False,True,pygame.sprite.collide_mask)
            for each_enemy_1 in enemy_1_myplane_bullet_collide:    # 字典，value是列表；each是key【enemy_1】
                for each_bullet in enemy_1_myplane_bullet_collide[each_enemy_1]:    # 抓取列表中每一个子弹
                    each_enemy_1.get_hurt(each_bullet.power)


            ## enemy1边界碰撞与死亡演示
            for each in enemy_1_group:
                if each.edge_collide():
                    enemy_1_group.remove(each)
                    continue
                temp = each.check_die()
                if temp == 2:
                    enemy1_down_sound.play()
                elif temp:
                    enemy_1_group.remove(each)
                    continue
                each.move()
                screen.blit(each.image,each.rect)


            # bonus    # 0子弹数量，1子弹类型，2僚机，3大招，4血，5蓝
            if loop == frequancy and len(bonus_group) <= 1:
                temp = get_bonus_born_position()
                if int(choice("01")):
                    bonus_group.add(Bonus(ratio,temp[0],temp[1],screen_size,int(choice("45"))))
                    #bonus_group.add(Bonus(ratio,temp[0],temp[1],screen_size,int(choice("2345"))))
                else:
                    bonus_group.add(Bonus(ratio,temp[0],temp[1],screen_size,int(choice("01")),int(choice("012"))))

            for each in bonus_group:
                each.move()
                if not each.active:
                    bonus_group.remove(each)
                if not each.flashing:
                    screen.blit(each.image,each.rect)
                elif loop%20 in range(10):
                    screen.blit(each.image,each.rect)
                #pygame.draw.circle(screen,(0,0,0),each.aim,100,0)    # 测试用

            bonus_myplane_collide = pygame.sprite.spritecollide(me,\
                                bonus_group,True,pygame.sprite.collide_mask)
            if bonus_myplane_collide:
                for each in bonus_myplane_collide:    # 此处是碰撞的bonus集合
                    me.get_bonus(each.type,each.num)
                    if each.type == 0:
                        get_bullet_sound.play()
                    elif each.type == 1:
                        get_bullet_sound.play()
                    elif each.type == 2:#
                        get_upgrade_sound.play()
                    elif each.type == 3:#
                        get_bomb_sound.play()
                    elif each.type == 4 or 5:#
                        get_supply_sound.play()


            # 画子弹
            for each in myplane_bullet_group:
                screen.blit(each.image,each.rect)


            # 画血槽可以考虑用递归？画格子的。好像也没必要
            if me.active and me.hp > 0:
                # 绘制矩形(绘制在哪，什么颜色，矩形的范围left top width height，矩形边框的大小)
                if me.hp/me.hp_max > 0.3:
                    pygame.draw.rect(screen,(100,255,100),\
                                        (me.rect.center[0]-50*ratio, me.rect.center[1]-int(100*ratio),\
                                        100*(me.hp/me.hp_max)*ratio, int(10*ratio)),0)
                elif loop%20 in range(10):
                    pygame.draw.rect(screen,(255,60,60),\
                                        (me.rect.center[0]-50*ratio, me.rect.center[1]-int(100*ratio),\
                                        100*(me.hp/me.hp_max)*ratio, int(10*ratio)),0)
                pygame.draw.rect(screen,(0,0,0),\
                                    (me.rect.center[0]-50*ratio, me.rect.center[1]-int(100*ratio),\
                                    100*ratio,int(10*ratio)),1)
                # (文本，拒绝锯齿，颜色)，没有居中设置，要讨巧设置
                me_hp_text = font_fs(int(10*ratio)).render("%d/%d" % (int(me.hp),me.hp_max),True,(0,0,0))
                me_hp_text_rect = me_hp_text.get_rect()
                screen.blit(me_hp_text,\
                            (me.rect.center[0]-me_hp_text_rect[2]/2,me.rect.center[1]-int(100*ratio)))

                # 蓝槽
                pygame.draw.rect(screen,(70,200,255),\
                                    (me.rect.center[0]-50*ratio, me.rect.center[1]-int(100*ratio)+int(10*ratio),\
                                    100*(me.sp/me.sp_max)*ratio,int(10*ratio)),0)
                pygame.draw.rect(screen,(0,0,0),\
                                    (me.rect.center[0]-50*ratio, me.rect.center[1]-int(100*ratio)+int(10*ratio),\
                                    100*ratio,int(10*ratio)),1)
                # (文本，拒绝锯齿，颜色)，没有居中设置，要讨巧设置
                me_sp_text = font_fs(int(10*ratio)).render("%d/%d" % (int(me.sp),me.sp_max),True,(0,0,0))
                me_sp_text_rect = me_sp_text.get_rect()
                screen.blit(me_sp_text,\
                            (me.rect.center[0]-me_sp_text_rect[2]/2,me.rect.center[1]-int(100*ratio)+int(10*ratio)))


            if me.hurting == True:
                if loop%6 in range(3):
                    screen.blit(me.image,me.rect)
                    if len(weiqi_group) == weiqi_num:
                        alpha_num = 0
                        for each in weiqi_group:
                            alpha_num += 255/weiqi_num
                            set_image_alpha(each,screen,alpha_num)
                    else:
                        for each in weiqi_group:
                            screen.blit(each.image,each.rect)
            else:
                if len(weiqi_group) == weiqi_num:
                    alpha_num = 0
                    for each in weiqi_group:
                        alpha_num += 255/weiqi_num
                        set_image_alpha(each,screen,alpha_num)
                else:
                    for each in weiqi_group:
                        screen.blit(each.image,each.rect)
                screen.blit(me.image,me.rect)


            # UI
            ##暂停按钮
            if mouse_pos[0] in range(screen_size[0]-65-20,screen_size[0]-20) and\
                        mouse_pos[1] in range(30,70) and switch_mouse_left:
                pause_button = pause_pressed
            else:
                pause_button = pause_nor
            screen.blit(pause_button,(screen_size[0]-65-20,30))

    
    
    
    # 把screen2上面的透明图层画到screen上        
    screen.blit(screen2,(0,0))
    #pygame.display.update()
    pygame.display.flip()
    clock.tick(frequancy)
    # 然后while True循环继续