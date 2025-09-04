import pygame
import math
from core.settings import Settings
import os


class Enemy(pygame.sprite.Sprite):
    SPRITE_SIZE = 16
    GUARD_SPEED = 1
    DETECTION_RANGE = 64
    FOV = 90

    def __init__(self, base_x=0, base_y=0, target_x=0, target_y=0):
        super().__init__()
        self.sprite_path = os.path.join("assets", "entities", "enemy_sprite.png")
        self.sprite_sheet = pygame.image.load(self.sprite_path)
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.get_image(0, 0)
        self.rect = self.image.get_rect()

        # 0 = droite
        # 90 = bas
        # 180 = gauche
        # 270 = haut
        self.angle = 0.0

        self.path = "go"
        self.x = base_x
        self.y = base_y
        self.base_x = base_x
        self.base_y = base_y
        self.target_x = target_x
        self.target_y = target_y
        self.alertness = 0

        self.exclamation_mark = pygame.image.load('assets/other/exclamation_mark.png')
        self.image_exclamation_mark = pygame.Surface([16, 16])
        self.image_exclamation_mark.blit(self.exclamation_mark, (0, 0), (0, 0, 16, 16))
        self.image_exclamation_mark.set_colorkey([0, 0, 0])

    def get_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0, 0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    def draw_detection_area(self, surface):
        left_angle = self.angle - math.radians(self.FOV / 2)
        right_angle = self.angle + math.radians(self.FOV / 2)

        left_endpoint = (self.rect.center[0] + self.DETECTION_RANGE * math.cos(left_angle),
                         self.rect.center[1] + self.DETECTION_RANGE * math.sin(left_angle))
        right_endpoint = (self.rect.center[0] + self.DETECTION_RANGE * math.cos(right_angle),
                          self.rect.center[1] + self.DETECTION_RANGE * math.sin(right_angle))

        s = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(s, (255, 0, 0, 64), [self.rect.center, left_endpoint, right_endpoint])
        surface.blit(s, (0, 0))

    def draw_exclamation_mark(self, surface):
        if self.alertness > 0:
            x = self.rect.centerx - self.image_exclamation_mark.get_width() / 2
            y = self.rect.top - self.image_exclamation_mark.get_height()
            surface.blit(self.image_exclamation_mark, (x, y))

    def is_player_detected(self, player, clock):
        settings = Settings()
        player_center = player.center

        dx = player_center[0] - self.rect.centerx
        dy = player_center[1] - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > self.DETECTION_RANGE:
            self.alertness = 0
            return False

        angle_to_player = math.atan2(dy, dx)
        angle_diff = (angle_to_player - self.angle + math.pi) % (2 * math.pi) - math.pi

        if abs(angle_diff) <= math.radians(self.FOV / 2):
            self.alertness += clock.tick(settings.FPS)
        else:
            self.alertness = 0

        return self.alertness >= 200

    def update(self):
        dx, dy = 0, 0

        if self.path == "go":
            if not math.isclose(self.x, self.target_x, abs_tol=self.GUARD_SPEED):
                dx = self.GUARD_SPEED if self.x < self.target_x else -self.GUARD_SPEED
            elif not math.isclose(self.y, self.target_y, abs_tol=self.GUARD_SPEED):
                dy = self.GUARD_SPEED if self.y < self.target_y else -self.GUARD_SPEED
            else:
                self.path = "back"

        elif self.path == "back":
            if not math.isclose(self.y, self.base_y, abs_tol=self.GUARD_SPEED):
                dy = self.GUARD_SPEED if self.y < self.base_y else -self.GUARD_SPEED
            elif not math.isclose(self.x, self.base_x, abs_tol=self.GUARD_SPEED):
                dx = self.GUARD_SPEED if self.x < self.base_x else -self.GUARD_SPEED
            else:
                self.path = "go"

        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

        # Change l'angle de la zone de détection lors du déplacement du garde
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
