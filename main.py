# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame

from ball import Ball

pygame.init()

SIZE = WIDTH, HEIGHT = 1800, 1000
BLACK = 0, 0, 0

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

ball = Ball()

mouse = pygame.mouse.get_pos()
running = True
while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.MOUSEBUTTONDOWN:
                if ball.collidemouse(pygame.mouse.get_pos()):
                    ball.grab = True
            case pygame.MOUSEBUTTONUP:
                ball.grab = False
    
    screen.fill(BLACK)
    ball.update(mouse, screen)
    mouse = pygame.mouse.get_pos()
    pygame.display.update()
    clock.tick(60)
