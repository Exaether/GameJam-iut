import pygame

import math


class Compass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.arrow = pygame.image.load("./assets/other/arrow.png").convert_alpha()
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.angle = 0
        ## coordonnées du centre de l'écran
        self.x = x
        self.y = y

    def update(self, player, items):
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
                loot = item
                rel_loot_x = rel_pos_x
                rel_loot_y = rel_pos_y

        # normaliser les distances
        r = math.hypot(rel_loot_x, rel_loot_y)
        rel_loot_x /= r
        rel_loot_y /= r

        angle = -math.degrees(math.atan2(rel_loot_y, rel_loot_x))

        self.image = pygame.transform.rotate(self.arrow, angle)

        self.rect = self.arrow.get_rect()
        self.rect.center = (self.x + rel_loot_x * 200,
                            self.y + rel_loot_y * 200)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
