import pygame

class ExitDoor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.x = 2522
        self.y = 150
        self.rect = pygame.Rect(self.x, self.y, 48, 24)

    def draw(self, surface, camera):
        rect = pygame.Rect(self.rect.left + camera[0], self.rect.top + camera[1], 48, 24)

        # Surface temporaire avec canal alpha
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        # Dessin du rectangle vert avec alpha 80
        pygame.draw.rect(temp_surface, (0, 255, 0, 80), temp_surface.get_rect())

        # Blit sur la surface principale
        surface.blit(temp_surface, rect.topleft)