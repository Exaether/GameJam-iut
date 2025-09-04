import pygame
from .enemy import Enemy

class EnemyGroup(pygame.sprite.Group):
    def add(self, *sprites):
        for sprite in sprites:
            if not isinstance(sprite, Enemy):
                raise TypeError("Seul le type Enemy peut être ajouté au groupe EnemyGroup.")
        super().add(*sprites)

    def draw(self, surface, bgsurf = None, special_flags = 0):
        super().draw(surface)
        for enemy in self.sprites():
            if isinstance(enemy, Enemy):
                enemy.draw_detection_area(surface)
                enemy.draw_exclamation_mark(surface)
