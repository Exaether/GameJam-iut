"""
Object Player create for game one player 
"""
import pygame
from pygame.locals import *
import os 

class Player(pygame.sprite.Sprite):
    """
    Spawn player info
    """
    def __init__(self):
        super().__init__()
        
        image_path = os.path.join('image', 'knightLife.png')
        img = pygame.image.load(image_path).convert_alpha()

        self.name = "player"
        self.healPoint = 1
        self.images = []
        self.speed = 5
        self.player_width = img.get_width()
        self.player_height = img.get_height()

        
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
    
    def get_name(self):
        return self.name
    
    def get_healPoint(self):
        return self.healPoint
    
    def get_speed(self):
        return self.speed
    
    def get_player_width(self):
        return self.player_width
    
    def get_player_height(self):
        return self.player_height
    
    def hurt(self):
        self.healPoint-1
    
    