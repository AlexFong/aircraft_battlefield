#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame

screen_size_default = width,height = 1600,900

class Button(pygame.sprite.Sprite):    # 这里init不一定要用精灵吧
    def __init__(self,ratio,text="Button",text_size=48,text_color=(30,30,30),align="center",\
                    shape="rect",center=(300,80),size=(300,80),width=0,color=(50,150,255)):
        pygame.sprite.Sprite.__init__(self)
        
        self.ratio = ratio
        self.active = False


        self.text = text
        self.raw_text_size = text_size
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.text_color1 = text_color
        self.text_color2 = (int(text_color[0]*0.3),int(text_color[1]*0.3),int(text_color[2]*0.3))
        self.text_color = self.text_color1
        self.align = align
        
        self.shape = shape
        self.center = center
        self.raw_size = size
        self.size = self.raw_size
        self.rect = (int(center[0]-size[0]*0.5),int(center[1]-size[1]*0.5),size[0],size[1])
        self.width = width
        self.color1 = color
        self.color2 = (int(color[0]*0.8),int(color[1]*0.8),int(color[2]*0.9))
        self.color = self.color1
        
        self.shadow_color = (int(self.color[0]*0.3),int(self.color[1]*0.3),int(self.color[2]*0.5))
        self.shadow_rect = (self.rect[0]+5,self.rect[1]-5,self.rect[2],self.rect[3])
        self.shadow_width = 0
        

    def draw(self,screen):
        self.shadow_color = (int(self.color[0]*0.3),int(self.color[1]*0.3),int(self.color[2]*0.5))
        self.shadow_rect = (self.rect[0]+5,self.rect[1]-5,self.rect[2],self.rect[3])
        self.shadow_width = 0
        
        # 看看是要直接搞还是封装成方法
        pygame.draw.rect(screen,self.shadow_color,self.shadow_rect,self.shadow_width)
        pygame.draw.rect(screen,self.color,self.rect,self.width)
        
        # (文本，拒绝锯齿，颜色)，没有居中设置，要讨巧设置
        button_text = self.font.render(self.text,True,self.text_color)
        button_text_rect = button_text.get_rect()
        # 文字挂点是(left,top)
        screen.blit(button_text,(self.rect[0] + self.rect[2]*0.5 - button_text_rect[2]*0.5,\
                                 self.rect[1] + self.rect[3]*0.5 - button_text_rect[3]*0.55))
        
    def on_button(self,mouse_pos):
        if mouse_pos[0] in range(self.rect[0],self.rect[0]+self.rect[2]) and\
                            mouse_pos[1] in range(self.rect[1],self.rect[1]+self.rect[3]):
            return True
        else:
            return False
        

        
class Setting_touch_bar(pygame.sprite.Sprite):
    def __init__(self,ratio,value,text="设置",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2,100),size=(screen_size_default[0]/2,50),color=(50,50,50,150)):
        pygame.sprite.Sprite.__init__(self)
        
        self.value = value
        self.ratio = ratio
        self.active = False
        
        self.text = text
        self.raw_text_size = text_size
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.text_color1 = text_color
        self.text_color2 = (int(text_color[0]*0.3),int(text_color[1]*0.3),int(text_color[2]*0.3))
        self.text_color = self.text_color1
        
        #self.raw_center = center
        self.center = (center[0], center[1])
        
        self.raw_size = size
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)

        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                    int(self.center[1]-self.size[1]*0.5),self.size[0],self.size[1])

        self.color1 = color
        self.color2 = (int(color[0]*0.8),int(color[1]*0.8),int(color[2]*0.9))
        self.color = self.color1
        
        
        self.bar_empty_rect = (screen_size_default[0]*0.57*self.ratio, self.rect[1]+self.rect[3]*0.4,\
                               screen_size_default[0]*0.12*self.ratio, self.rect[3]*0.2)
        self.bar_empty_color = (20,20,20)
        
        self.bar_fill_rect = (screen_size_default[0]*0.57*self.ratio, self.rect[1]+self.rect[3]*0.4,\
                              screen_size_default[0]*0.12*self.ratio*self.value, self.rect[3]*0.2)
        self.bar_fill_color = (100,150,255)
        self.fill_point = int(self.bar_fill_rect[0]+self.bar_fill_rect[2]),\
                        int(self.bar_fill_rect[1]+self.bar_fill_rect[3]*0.5)

        self.num_position = (screen_size_default[0]*0.715*self.ratio,\
                                self.rect[1] + self.rect[3]*0.5)
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect,0)
        
        pygame.draw.rect(screen,self.bar_empty_color,self.bar_empty_rect,0)
        pygame.draw.rect(screen,self.bar_fill_color,self.bar_fill_rect,0)
        pygame.draw.circle(screen,(255,255,255),self.fill_point,int(self.rect[3]*0.2))
        
        
        # (文本，拒绝锯齿，颜色)，没有居中设置，要讨巧设置
        setting_text = self.font.render(self.text,True,self.text_color)
        setting_text_rect = setting_text.get_rect()
        screen.blit(setting_text,(self.rect[0] + self.rect[2]*0.05,\
                                 self.rect[1] + self.rect[3]*0.5 - setting_text_rect[3]*0.55))# 文字挂点是(left,top)
        
        num_text = self.font.render(str(int(self.value*100)),True,self.text_color)
        num_text_rect = num_text.get_rect()
        screen.blit(num_text,(self.num_position[0] - num_text_rect[2]*0.5,\
                                self.num_position[1] - num_text_rect[3]*0.55))
        
    def on_button(self,mouse_pos):
        if mouse_pos[0] in range(int(self.bar_empty_rect[0]-5*self.ratio),int(self.bar_empty_rect[0]+self.bar_empty_rect[2]+5*self.ratio)) and\
                mouse_pos[1] in range(int(self.bar_empty_rect[1]-5*self.ratio),int(self.bar_empty_rect[1]+self.bar_empty_rect[3]+5*self.ratio)):
            return True
        else:
            return False
        
    def change(self,mouse_pos):
        self.value = round((mouse_pos[0] - self.bar_empty_rect[0])/self.bar_empty_rect[2],2)
        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0
            
        self.bar_fill_rect = (self.bar_fill_rect[0],self.bar_fill_rect[1],\
                              self.bar_empty_rect[2] * self.value,self.bar_fill_rect[3])
        self.fill_point = int(self.bar_fill_rect[0]+self.bar_fill_rect[2]),self.fill_point[1]
        
        
class Setting_drawer(pygame.sprite.Sprite):
    def __init__(self,ratio,value,list,text="设置",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2,100),size=(800,50),color=(50,50,50,150)):
        pygame.sprite.Sprite.__init__(self)
        
        self.value = value
        self.list = list
        self.ratio = ratio
        self.active = False

        self.text = text
        self.raw_text_size = text_size
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.text_color1 = text_color
        self.text_color2 = (int(text_color[0]*0.3),int(text_color[1]*0.3),int(text_color[2]*0.3))
        self.text_color = self.text_color1
        
        #self.raw_center = center
        self.center = (center[0]*self.ratio, center[1]*self.ratio)
        self.raw_size = size
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)
        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                    int(self.center[1]-self.size[1]*0.5),self.size[0],self.size[1])
        self.color1 = color
        self.color2 = (int(color[0]*0.8),int(color[1]*0.8),int(color[2]*0.9))
        self.color = self.color1
        
        if len(self.list) > 10:
            self.list_num = 10
            if self.list.index(self.value) + self.list_num < len(self.list):
                self.list_head_index = self.list.index(self.value)
            else:
                self.list_head_index = len(self.list) - 10
        else:
            self.list_num = len(self.list)
            self.list_head_index = 0
        
        self.raw_list_per_height = 40
        self.list_per_height = self.raw_list_per_height * self.ratio
        self.top_rect = (screen_size_default[0]*0.57*self.ratio,self.rect[1]+5*self.ratio,\
                        screen_size_default[0]*0.16*self.ratio,self.list_per_height)
        self.top_color = (100,150,255)
        
        self.list_rect = (screen_size_default[0]*0.57*self.ratio,self.top_rect[1] + self.list_per_height + 5*self.ratio,\
                        screen_size_default[0]*0.16*self.ratio,self.list_num*self.list_per_height)
        self.list_color = (0,40,80)
        self.bar_height = self.list_per_height*10*10/len(self.list)


    def draw_top(self,screen):
        # 底色
        pygame.draw.rect(screen,self.color,self.rect,0)
        
        setting_text = self.font.render(self.text,True,self.text_color)
        setting_text_rect = setting_text.get_rect()
        screen.blit(setting_text,(self.rect[0] + self.rect[2]*0.05,\
                                    self.rect[1] + self.rect[3]*0.5 - setting_text_rect[3]*0.5))# 文字挂点是(left,top)

        # top选项框
        pygame.draw.rect(screen,self.top_color,self.top_rect,0)
        temp_text = self.font.render(str(self.value),True,self.text_color)
        temp_text_rect = temp_text.get_rect()
        screen.blit(temp_text,(self.top_rect[0]+10*self.ratio,\
                                self.top_rect[1] + self.top_rect[3]*0.5 - temp_text_rect[3]*0.5))
        
    def draw_list(self,screen):
        # 画每一个选项框
        pygame.draw.rect(screen,self.list_color,self.list_rect,0)
        i = 1
        for each in self.list[self.list_head_index : self.list_head_index + self.list_num]:
            if each == self.value:
                pygame.draw.rect(screen,self.top_color,(self.top_rect[0]+5*self.ratio, \
                                                        self.top_rect[1]+self.list_per_height*i+7*self.ratio,\
                                                        self.top_rect[2]-25*self.ratio, \
                                                        self.list_per_height-4*self.ratio),0)
            temp_text = self.font.render(str(each),True,self.text_color)
            temp_text_rect = temp_text.get_rect()
            screen.blit(temp_text,(self.top_rect[0]+10*self.ratio,\
                                    self.top_rect[1] + self.list_per_height*(i+0.5) + 5*self.ratio - temp_text_rect[3]*0.5))
            i += 1
        
        # 画滚动条
        if len(self.list) > 10:    # 只有大于10条才画出来
            pygame.draw.rect(screen,(200,200,200),(self.top_rect[0]+self.top_rect[2]-15*self.ratio,self.list_rect[1],\
                                                    15*self.ratio,self.list_num*self.list_per_height),0)
            pygame.draw.rect(screen,(100,100,100),(self.top_rect[0]+self.top_rect[2]-15*self.ratio,\
                self.list_rect[1]+self.list_head_index*(self.list_num*self.list_per_height-self.bar_height)/(len(self.list)-10),\
                15*self.ratio,self.bar_height),0)

    def on_button(self,mouse_pos):
        if mouse_pos[0] in range(int(self.top_rect[0]-5*self.ratio),int(self.top_rect[0]+self.top_rect[2]+5*self.ratio)) and\
                    mouse_pos[1] in range(int(self.top_rect[1]-5*self.ratio),int(self.top_rect[1]+self.top_rect[3]+5*self.ratio)):
            return True
        else:
            return False
        
    def on_list(self,mouse_pos):
        i = 0
        result = False
        for each in self.list[self.list_head_index : self.list_head_index + self.list_num]:
            if mouse_pos[0] in range(int(self.list_rect[0]),int(self.list_rect[0] + self.list_rect[2]-15*self.ratio)) and\
                mouse_pos[1] in range(int(self.list_rect[1]+self.list_per_height*i),\
                                        int(self.list_rect[1] + self.list_per_height*(i+1))):
                result = i + self.list_head_index + 1
                break
            i += 1
        return result

    def on_bar(self,mouse_pos):
        if mouse_pos[0] in range(int(self.top_rect[0]+self.top_rect[2]-15*self.ratio),int(self.top_rect[0]+self.top_rect[2])) and\
                    mouse_pos[1] in range(int(self.list_rect[1]),int(self.list_rect[1]+self.list_num*self.list_per_height)):
            return True
        else:
            return False


    def change(self,mouse_pos):
        self.value = round((mouse_pos[0] - self.bar_empty_rect[0])/self.bar_empty_rect[2],2)
        if self.value > 1:
            self.value = 1
        elif self.value < 0:
            self.value = 0
            
        self.bar_fill_rect = (self.bar_fill_rect[0],self.bar_fill_rect[1],\
                              self.bar_empty_rect[2] * self.value,self.bar_fill_rect[3])
        self.fill_point = int(self.bar_fill_rect[0]+self.bar_fill_rect[2]),self.fill_point[1]
        
    def change_bar(self,mouse_pos):
        # 只判断y轴即可
        if mouse_pos[1] < int(self.list_rect[1] + 0.5*self.bar_height):
            self.list_head_index = 0
        elif mouse_pos[1] > int(self.list_rect[1] + self.list_num*self.list_per_height - 0.5*self.bar_height):
            self.list_head_index = len(self.list) - self.list_num
        else:
            # 小柱/(大柱/份数)
            self.list_head_index = int((mouse_pos[1] - int(self.list_rect[1] + 0.5*self.bar_height))\
                                        /(self.list_num*self.list_per_height - self.bar_height)*(len(self.list) - self.list_num))

            
class Setting_choice(pygame.sprite.Sprite):
    def __init__(self,ratio,list1,list2,key,text="设置",text_size=24,text_color=(255,255,255),\
                    center=(screen_size_default[0]/2,100),size=(screen_size_default[0]/2,50),color=(50,50,50,150)):
        pygame.sprite.Sprite.__init__(self)
        
        if key in list1:
            self.key = key
        else:
            self.key = list1[0]
        
        self.key_list = list1
        self.value_list = list2
        self.index = self.key_list.index(self.key)
        self.value = self.value_list[self.index]

        self.ratio = ratio

        self.text = text
        self.raw_text_size = text_size
        self.text_size = int(self.raw_text_size * self.ratio)
        self.font = pygame.font.Font("font/msyh.ttf",self.text_size)
        self.text_color1 = text_color
        self.text_color2 = (int(text_color[0]*0.3),int(text_color[1]*0.3),int(text_color[2]*0.3))
        self.text_color = self.text_color1
        
        self.center = center
        
        self.raw_size = size
        self.size = (self.raw_size[0]*self.ratio, self.raw_size[1]*self.ratio)

        self.rect = (int(self.center[0]-self.size[0]*0.5),\
                    int(self.center[1]-self.size[1]*0.5),self.size[0],self.size[1])

        self.color1 = color
        self.color2 = (int(color[0]*0.8),int(color[1]*0.8),int(color[2]*0.9))
        self.color = self.color1
        
        self.rawimage = pygame.image.load("images/arrow.png").convert_alpha()
        self.raw_rect = self.rawimage.get_rect()
        self.right_image = pygame.transform.smoothscale(self.rawimage,\
                            (int(self.raw_rect.width*self.ratio),int(self.raw_rect.height*self.ratio)))
        self.right_image_rect = self.right_image.get_rect()
        self.right_image_rect.center = (screen_size_default[0]*0.72,self.rect[1]+self.rect[3]*0.5)
        self.left_image = pygame.transform.rotate(self.right_image,180)
        self.left_image_rect = self.left_image.get_rect()
        self.left_image_rect.center = (screen_size_default[0]*0.58,self.rect[1]+self.rect[3]*0.5)

        self.key_position = (screen_size_default[0]*0.65*self.ratio,\
                                self.rect[1] + self.rect[3]*0.5)
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect,0)
        #print(self.text_size)
        # (文本，拒绝锯齿，颜色)，没有居中设置，要讨巧设置
        setting_text = self.font.render(self.text,True,self.text_color)
        setting_text_rect = setting_text.get_rect()
        screen.blit(setting_text,(self.rect[0] + self.rect[2]*0.05,\
                                 self.rect[1] + self.rect[3]*0.5 - setting_text_rect[3]*0.55))# 文字挂点是(left,top)
        
        key_text = self.font.render(self.key,True,self.text_color)
        key_text_rect = key_text.get_rect()
        screen.blit(key_text,(self.key_position[0] - key_text_rect[2]*0.5,\
                                self.key_position[1] - key_text_rect[3]*0.55))
        
        screen.blit(self.right_image,(self.right_image_rect[0],self.right_image_rect[1]))
        screen.blit(self.left_image,(self.left_image_rect[0],self.left_image_rect[1]))


    def on_button_left(self,mouse_pos):
        if mouse_pos[0] in range(int(self.left_image_rect[0]),int(self.left_image_rect[0]+self.left_image_rect[2])) and\
                mouse_pos[1] in range(int(self.left_image_rect[1]),int(self.left_image_rect[1]+self.left_image_rect[3])):
            return True
        else:
            return False

    def on_button_right(self,mouse_pos):
        if mouse_pos[0] in range(int(self.right_image_rect[0]),int(self.right_image_rect[0]+self.right_image_rect[2])) and\
                mouse_pos[1] in range(int(self.right_image_rect[1]),int(self.right_image_rect[1]+self.right_image_rect[3])):
            return True
        else:
            return False
        
    def change(self,value):
        self.index = self.index + value
        if self.index > len(self.key_list)-1:
            self.index = 0
        elif self.index < 0:
            self.index = len(self.key_list)-1
        self.key = self.key_list[self.index]
        self.value = self.value_list[self.index]

        
