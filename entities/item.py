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
        

    def draw_highlight(self, screen, screen_rect, color=(255, 255, 255, 180), thickness=3):
        # screen_rect est déjà ajusté à la caméra
        highlight_rect = screen_rect.inflate(thickness * 2, thickness * 2)
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)

        pygame.draw.rect(highlight_surface, color, highlight_surface.get_rect(), border_radius=100)  

        screen.blit(highlight_surface, highlight_rect.topleft)

    def draw(self, screen, camera):
        screen_pos = self.rect.move(camera)
        self.draw_highlight(screen, screen_pos)
        screen.blit(self.image, self.rect.move(camera))
        
