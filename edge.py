#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame

# 定义me的飞行边界edge
class Edge(pygame.sprite.Sprite):    # 继承
    def __init__(self,direction,left,top,width,height):
        pygame.sprite.Sprite.__init__(self)
        
        self.direction = direction
        
        # 用此方法来改变宽度和高度
        self.image = pygame.image.load("images/black.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.mask = pygame.mask.from_surface(self.image)
        