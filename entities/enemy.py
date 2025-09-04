import pygame
import math
from core.settings import Settings 

class Enemy(pygame.sprite.Sprite):

    SPRITE_SIZE = 16
    GUARD_SPEED = 0.1
    COLLISION_AREA_WIDTH = 16
    COLLISION_AREA_HEIGHT = 16
    
    def __init__(self, base_x=0, base_y=0, target_x=0, target_y=0):
        super().__init__()
        self.sprite_sheet = pygame.image.load('assets/entities/enemy_sprite.png')
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.direction = "right"
        self.path = "go" # "go" à l'aller vers les coordonnées target et "back" au retour
        self.x = base_x
        self.y = base_y
        self.base_x = base_x
        self.base_y = base_y
        self.target_x = target_x
        self.target_y = target_y
        self.detection_area = pygame.rect.Rect(self.rect.left + self.SPRITE_SIZE, self.rect.top, self.COLLISION_AREA_WIDTH, self.COLLISION_AREA_HEIGHT)

    """
    Récupère l'image souhaitée sur la feuille de sprite
    """
    def get_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0, 0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    """
    Change la direction ou regarde l'entité
    """
    def set_direction(self, direction="right"):
        if direction == "right":
            self.direction = "right"
            self.get_image(0, 0)
            self.rect = self.image.get_rect()
        elif direction == "left":
            self.direction = "left"
            self.get_image(16, 0)
            self.rect = self.image.get_rect()

    def draw_detection_area(self, surface):
        shape_surf = pygame.Surface(pygame.Rect(self.detection_area).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (255, 0, 0, 64), shape_surf.get_rect())
        surface.blit(shape_surf, self.detection_area)

    def is_detection_area_colliding(self, rect):
        return self.detection_area.colliderect(rect)

    def update(self):
        # Va vers les coordonnées target_x puis target_y
        if self.path == "go":
            if not math.isclose(self.x, self.target_x, abs_tol=self.GUARD_SPEED):
                if self.x < self.target_x:
                    self.x += self.GUARD_SPEED
                    self.set_direction("right")
                else:
                    self.x -= self.GUARD_SPEED
                    self.set_direction("left")
            elif not math.isclose(self.y, self.target_y, abs_tol=self.GUARD_SPEED):
                if self.y < self.target_y:
                    self.y += self.GUARD_SPEED
                else:
                    self.y -= self.GUARD_SPEED
            else:
                self.path = "back"

        # Reviens vers les coordonnées base_y puis base_x (refait donc le même chemin mais dans l'autre sens)
        elif self.path == "back":
            if not math.isclose(self.y, self.base_y, abs_tol=self.GUARD_SPEED):
                if self.y < self.base_y:
                    self.y += self.GUARD_SPEED
                else:
                    self.y -= self.GUARD_SPEED
            elif not math.isclose(self.x, self.base_x, abs_tol=self.GUARD_SPEED):
                if self.x < self.base_x:
                    self.x += self.GUARD_SPEED
                    self.set_direction("right")
                else:
                    self.x -= self.GUARD_SPEED
                    self.set_direction("left")
            else:
                self.path = "go"

        self.rect.topleft = (self.x, self.y)
        if self.direction == "right":
            self.detection_area = pygame.rect.Rect(self.rect.left + self.SPRITE_SIZE, self.rect.top, self.COLLISION_AREA_WIDTH, self.COLLISION_AREA_HEIGHT)
        elif self.direction == "left":
            self.detection_area = pygame.rect.Rect(self.rect.left - self.SPRITE_SIZE, self.rect.top, self.COLLISION_AREA_WIDTH, self.COLLISION_AREA_HEIGHT)