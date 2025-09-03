# !/usr/bin/env python
# -*- coding:utf-8 -*-


import pygame
from math import sqrt

from vectors import Vector
from physics import air_and_g


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = 900, 500
        self.grab = False
        self.speed = Vector(0, 0)
        self.weight = 0.15
    
    def move(self):
        self.rect.move_ip(self.speed.x, self.speed.y)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self, mouse, screen):
        if self.grab:
            mousepos = pygame.mouse.get_pos()
            x = mousepos[0] - mouse[0]
            y = mousepos[1] - mouse[1]
            self.speed = Vector(x, y)
        else:
            self.speed = air_and_g(self.speed, self.weight)
        
        self.move()
        screenrect = screen.get_rect()
        if self.rect.top < 0:
            self.speed.y = -self.speed.y
            self.rect.top = 0
        
        if self.rect.bottom > screenrect.bottom:
            self.speed.y = -self.speed.y
            self.rect.bottom = screenrect.bottom
        
        if self.rect.left < 0:
            self.speed.x = -self.speed.x
            self.rect.left = 0
        
        if self.rect.right > screenrect.right:
            self.speed.x = -self.speed.x
            self.rect.right = screenrect.right
        
        self.draw(screen)
    
    def collidemouse(self, mouse):
        radius = self.rect.width//2
        mousedist = sqrt((self.rect.center[0] - mouse[0])**2 + (self.rect.center[1] - mouse[1])**2)
        return radius >= mousedist

