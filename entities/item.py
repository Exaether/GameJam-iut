import pygame

from random import randint
from math import sin, pi
from paths import get_asset_path

PULSATION_DURATION = 0.2
PAUSE_BETWEEN_PULSATIONS = 0.1
PAUSE_BETWEEN_CYCLE = 1.0
PULSATION_CYCLE = 2 * PULSATION_DURATION + PAUSE_BETWEEN_PULSATIONS + PAUSE_BETWEEN_CYCLE
PULSATION_AMPLITUDE_PERCENT = 0.2
ORIGINAL_SCALE_PERCENT = 1.0


class Item(pygame.sprite.Sprite):
    """Item objectif du joueur"""

    def __init__(self, x, y):
        super().__init__()
        img_number = randint(1, 12)
        img_path = get_asset_path("items", f"{img_number}.png")

        self.image = pygame.image.load(img_path).convert_alpha()
        self.pickable = True
        self.item_width = self.image.get_width()
        self.item_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.pulse_timer = 0

    @staticmethod
    def get_pulse_scale():
        t = pygame.time.get_ticks() / 1000.0
        t_cycle = t % PULSATION_CYCLE

        # Animation de deux pulsations rapides puis on marque une pause
        if 0 <= t_cycle < PULSATION_DURATION:
            pulsation_scale = ORIGINAL_SCALE_PERCENT + PULSATION_AMPLITUDE_PERCENT * sin(
                pi * (t_cycle / PULSATION_DURATION))
        # pause entre les deux pulsations
        elif PULSATION_DURATION <= t_cycle < PULSATION_DURATION + PAUSE_BETWEEN_PULSATIONS:
            pulsation_scale = ORIGINAL_SCALE_PERCENT
        # 2ème pulsation
        elif PULSATION_DURATION + PAUSE_BETWEEN_PULSATIONS <= t_cycle < 2 * PULSATION_DURATION + PAUSE_BETWEEN_PULSATIONS:
            t2 = t_cycle - (PULSATION_DURATION + PAUSE_BETWEEN_PULSATIONS)
            pulsation_scale = ORIGINAL_SCALE_PERCENT + PULSATION_AMPLITUDE_PERCENT * sin(pi * (t2 / PULSATION_DURATION))
        # pause entre deux cycles de pulsation
        else:
            pulsation_scale = ORIGINAL_SCALE_PERCENT

        return pulsation_scale

    @staticmethod
    def draw_highlight(screen, screen_rect, color=(255, 255, 255, 180), thickness=3,
                       pulsation_scale=ORIGINAL_SCALE_PERCENT):
        # screen_rect est déjà ajusté à la caméra
        highlight_rect = screen_rect.inflate(thickness * 2, thickness * 2)

        # Appliquer la pulsation sur le highlight
        center = highlight_rect.center
        new_width = int(highlight_rect.width * pulsation_scale)
        new_height = int(highlight_rect.height * pulsation_scale)
        highlight_rect = pygame.Rect(0, 0, new_width, new_height)
        highlight_rect.center = center

        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)

        pygame.draw.rect(highlight_surface, color, highlight_surface.get_rect(), border_radius=100)

        screen.blit(highlight_surface, highlight_rect.topleft)

    def draw(self, screen, camera):
        pulsation_scale = Item.get_pulse_scale()
        screen_pos = self.rect.move(camera)

        # Dessiner le highlight en pulsation
        Item.draw_highlight(screen, screen_pos, pulsation_scale=pulsation_scale)

        # Dessiner l'item en pulsation
        self.__draw_item(screen, screen_pos, pulsation_scale)
        

    def __draw_item(self, screen, screen_pos, pulsation_scale):
        image = self.image
        if pulsation_scale != ORIGINAL_SCALE_PERCENT:
            new_w = int(self.item_width * pulsation_scale)
            new_h = int(self.item_height * pulsation_scale)
            image = pygame.transform.smoothscale(self.image, (new_w, new_h))
            img_rect = image.get_rect(center=screen_pos.center)
        else:
            img_rect = screen_pos
        screen.blit(image, img_rect)    