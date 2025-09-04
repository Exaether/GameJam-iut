import pygame
from pygame.locals import *
import os
import random

# Dossier du script courant
BASE_DIR = os.path.dirname(__file__)

"Item objectif du joueur"
class Item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img_number = random.randint(1, 12)
        img_path = os.path.join("assets", "items", f"{img_number}.png")

        self.image = pygame.image.load(img_path).convert_alpha()
        self.pickable = True
        self.item_width = self.image.get_width()
        self.item_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = x, y
