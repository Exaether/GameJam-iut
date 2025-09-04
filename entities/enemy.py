import pygame
import math
from core.settings import Settings 
import os

class Enemy(pygame.sprite.Sprite):

    SPRITE_SIZE = 16
    GUARD_SPEED = 1
    COLLISION_AREA_WIDTH = 64
    COLLISION_AREA_HEIGHT = 128

    def __init__(self, base_x=0, base_y=0, target_x=0, target_y=0):
        super().__init__()
        self.sprite_path = os.path.join("assets", "entities", "enemy_sprite.png")
        self.sprite_sheet = pygame.image.load(self.sprite_path)
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
        self.detection_area = pygame.Rect(0, 0, 0, 0)
        self.alertness = 0
        self.exclamation_mark = pygame.image.load('assets/other/exclamation_mark.png')
        self.image_exclamation_mark = pygame.Surface([16, 16])
        self.image_exclamation_mark.blit(self.exclamation_mark, (0, 0), (0, 0, 16, 16))
        self.image_exclamation_mark.set_colorkey([0, 0, 0])

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
        else:
            self.direction = direction

    """
    Dessine la zone de détection du garde
    """
    def draw_detection_area(self, surface):
        shape_surf = pygame.Surface(pygame.Rect(self.detection_area).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (255, 0, 0, 64), shape_surf.get_rect())
        surface.blit(shape_surf, self.detection_area)

    """
    Dessine un point d'exclamation au dessus du garde si le joueur est dans sa zone de détection
    """
    def draw_exclamation_mark(self, surface):
        if self.alertness> 0:
            x = self.rect.centerx - self.image_exclamation_mark.get_width()/2
            y = self.rect.top - self.image_exclamation_mark.get_height()
            surface.blit(self.image_exclamation_mark, (x, y))

    def is_player_detected(self, player, clock):
        settings = Settings()
        if self.detection_area.colliderect(player):
            self.alertness += clock.tick(settings.FPS)
        else:
            self.alertness = 0
        return self.alertness >= 200 # temps en millisecondes avant que le joueur se fasse attraper

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
                    self.set_direction("down")
                else:
                    self.y -= self.GUARD_SPEED
                    self.set_direction("up")
            else:
                self.path = "back"

        # Reviens vers les coordonnées base_y puis base_x (refait donc le même chemin mais dans l'autre sens)
        elif self.path == "back":
            if not math.isclose(self.y, self.base_y, abs_tol=self.GUARD_SPEED):
                if self.y < self.base_y:
                    self.y += self.GUARD_SPEED
                    self.set_direction("down")
                else:
                    self.y -= self.GUARD_SPEED
                    self.set_direction("up")
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
            self.detection_area = pygame.Rect(self.rect.right,
                                                   self.rect.top + self.SPRITE_SIZE/2 - self.COLLISION_AREA_HEIGHT/2,
                                                   self.COLLISION_AREA_WIDTH,
                                                   self.COLLISION_AREA_HEIGHT)
        elif self.direction == "left":
            self.detection_area = pygame.Rect(self.rect.left - self.COLLISION_AREA_WIDTH,
                                                   self.rect.top + self.SPRITE_SIZE/2 - self.COLLISION_AREA_HEIGHT/2,
                                                   self.COLLISION_AREA_WIDTH,
                                                   self.COLLISION_AREA_HEIGHT)
        elif self.direction == "down":
            self.detection_area = pygame.Rect(self.rect.left + self.SPRITE_SIZE/2 - self.COLLISION_AREA_HEIGHT/2,
                                                   self.rect.bottom,
                                                   self.COLLISION_AREA_HEIGHT,
                                                   self.COLLISION_AREA_WIDTH)
        elif self.direction == "up":
            self.detection_area = pygame.Rect(self.rect.left + self.SPRITE_SIZE / 2 - self.COLLISION_AREA_HEIGHT/2,
                                                   self.rect.top - self.COLLISION_AREA_WIDTH,
                                                   self.COLLISION_AREA_HEIGHT,
                                                   self.COLLISION_AREA_WIDTH)