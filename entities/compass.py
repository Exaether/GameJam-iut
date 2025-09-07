import pygame

from math import hypot, degrees, atan2
from paths import get_asset_path


class Compass:
    def __init__(self, x, y):
        self.arrow = pygame.image.load(get_asset_path('other','arrow.png')).convert_alpha()
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.angle = 0
        ## coordonnées du centre de l'écran
        self.x = x
        self.y = y

    def update(self, player, items):
        rel_loot_x, rel_loot_y = Compass.__find_closest_item(player, items)
        rel_loot_x, rel_loot_y = Compass.__normalize_distance(rel_loot_x, rel_loot_y)
        angle = Compass.__calculate_angle(rel_loot_x, rel_loot_y)

        self.__update_image_position(angle, rel_loot_x, rel_loot_y)     

    @staticmethod
    def __find_closest_item(player, items):
        loot = items.sprites()[0]
        player_x = player.rect.centerx
        player_y = player.rect.centery
        # coordonées du trésor relatives au joueur
        rel_loot_x = loot.rect.centerx - player_x
        rel_loot_y = loot.rect.centery - player_y
        # recherche du trésor le plus proche
        for item in items.sprites():
            rel_pos_x = item.rect.centerx - player_x
            rel_pos_y = item.rect.centery - player_y
            if abs(rel_pos_x) + abs(rel_pos_y) < abs(rel_loot_x) + abs(rel_loot_y):
                rel_loot_x = rel_pos_x
                rel_loot_y = rel_pos_y
        return rel_loot_x, rel_loot_y

    @staticmethod
    def __normalize_distance(rel_loot_x, rel_loot_y):
        r = hypot(rel_loot_x, rel_loot_y)
        rel_loot_x /= r
        rel_loot_y /= r
        return rel_loot_x, rel_loot_y

    @staticmethod
    def __calculate_angle(rel_loot_x, rel_loot_y):
        return -degrees(atan2(rel_loot_y, rel_loot_x))
         
    def __update_image_position(self, angle, rel_loot_x, rel_loot_y):
        self.image = pygame.transform.rotate(self.arrow, angle)

        self.rect = self.arrow.get_rect()
        self.rect.center = (self.x + rel_loot_x * 200,
                            self.y + rel_loot_y * 200)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
