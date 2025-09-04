import pygame
from pygame.locals import *
import os
import random

# Dossier du script courant
BASE_DIR = os.path.dirname(__file__)

"Item objectif du joueur"
class Item(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__() # initialisation d'un sprite de la class pygame.sprite.Sprite
        img_number = random.randint(1, 12)
        img_path = os.path.join("assets", "items", f"{img_number}.png") # Chemin complet vers l'image

        self.image = pygame.image.load(img_path).convert_alpha()
        self.pickable = True
        self.item_width = self.image.get_width()
        self.item_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def player_on_item(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom) and self.pickable == True:
            self.pickable = False
            return True # il faut supprimer dans le jeu le Item pour qu'il ne soit plus affiché
        return False
    
    def get_item_width(self):
        return self.item_width
    
    def get_item_height(self):
        return self.item_height
