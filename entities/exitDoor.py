import pygame

class ExitDoor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = 2530
        self.y = 150
        self.rect = pygame.Rect(self.x, self.y, 16, 16)