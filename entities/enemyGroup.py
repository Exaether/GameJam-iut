import pygame
from .enemy import Enemy

class EnemyGroup(pygame.sprite.Group):
    def add(self, *sprites):
        for sprite in sprites:
            if not isinstance(sprite, Enemy):
                raise TypeError("Seul le type Enemy peut être ajouté au groupe EnemyGroup.")
        super().add(*sprites)

    # TODO: Voir pour pas avoir besoin de passer le player
    def draw(self, surface, camera, player, bgsurf = None, special_flags = 0):
        for enemy in self.sprites():
            if isinstance(enemy, Enemy) and enemy.is_enemy_in_player_vision(player):
                enemy.draw(surface, camera)
                enemy.guard_speed = enemy.GUARD_DEFAULT_SPEED
            else : 
                enemy.guard_speed = enemy.GUARD_SPEED_OUT_VISION
