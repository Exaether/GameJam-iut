import pygame
import os
import random
from core.settings import Settings
from entities.vision_service import VisionService

class Enemy(pygame.sprite.Sprite):
    SPRITE_SIZE = 24
    GUARD_SPEED_OUT_VISION = 1.3
    GUARD_DEFAULT_SPEED = 1.8
    GUARD_SPEED_ON_DETECT = 2
    VISION_RANGE = 100
    VISION_ANGLE = 60
    ANIMATION_TICK = 15
    SIZE_EXCLAMATION_MARK = 24
    DETECTION_TIME_MS = 200

    def __init__(self, x_start, y_start, x_range_min, x_range_max, y_range_min, y_range_max, pattern_type="square"):
        super().__init__()
        self.__init_sprite()
        self.__init_position(x_start, y_start)
        self.__init_patrol_ranges(x_range_min, x_range_max, y_range_min, y_range_max)
        self.__init_patrol_steps(pattern_type)
        self.__init_alertness()
        self.__init_collision()
        self.vision_service = VisionService(self.VISION_RANGE, self.VISION_ANGLE)

    def __init_sprite(self, pattern_type="square"):
        sprite_path = os.path.join("assets", "entities", "enemy_sprite.png")
        self.sprite_sheet = pygame.image.load(sprite_path)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.SPRITE_SIZE*4, self.SPRITE_SIZE*2))
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.__get_image()    
        self.rect = self.image.get_rect()
        self.direction = "left"
        self.animation_tick = 0
        self.animation_sprite = 0
        self.guard_speed = self.GUARD_DEFAULT_SPEED
        self.pattern_type = pattern_type # type possible : ["fixe","square"]

    def __init_position(self, x, y):
        self.x = x
        self.y = y

    def __init_patrol_ranges(self, x_min, x_max, y_min, y_max):
        self.x_range_min = x_min
        self.x_range_max = x_max
        self.y_range_min = y_min
        self.y_range_max = y_max
        self.patrol_distance_x = random.randint(x_min, x_max)
        self.patrol_distance_y = random.randint(y_min, y_max)

    def __init_patrol_steps(self, pattern_type):
        if pattern_type == "square" or pattern_type == "fixe":    
            self.patrol_steps = [
                    {'direction': 'right', 'dx': 1, 'dy': 0},
                    {'direction': 'down', 'dx': 0, 'dy': 1},
                    {'direction': 'left', 'dx': -1, 'dy': 0},
                    {'direction': 'up', 'dx': 0, 'dy': -1}
                ]
        else:
            raise ValueError(f"Pattern type {pattern_type} not supported") # TODO : a rajouter des patterns de déplacement, idle...
        
        self.current_step_index = 0
        self.step_progress = 0

    def __init_alertness(self):
        self.alertness = 0
        exclamation_path = os.path.join("assets", "other", "exclamation_mark.png")
        self.exclamation_mark = pygame.image.load(exclamation_path)
        self.exclamation_mark = pygame.transform.scale(self.exclamation_mark, (self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK))
        self.image_exclamation_mark = pygame.Surface([self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK])
        self.image_exclamation_mark.blit(self.exclamation_mark, (0, 0), (0, 0, self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK))
        self.image_exclamation_mark.set_colorkey([0, 0, 0])

    def __init_collision(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.mask = pygame.mask.Mask((self.SPRITE_SIZE, self.SPRITE_SIZE), True)

    def __update_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0,0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    def __get_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0, 0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    def __get_sprite_y(self):
        sprite_y = 0
        if self.direction in ("right", "down"):
            sprite_y = 0
        else:
            sprite_y = self.SPRITE_SIZE
        return sprite_y

    def __get_sprite_x(self):
        return self.SPRITE_SIZE * self.animation_sprite

    def __update_sprite(self):
        self.__update_image(self.__get_sprite_x(), self.__get_sprite_y())

    def __advance_animation(self):
        if self.pattern_type == "square":
            self.animation_tick += 1
            if self.animation_tick == self.ANIMATION_TICK:
                self.animation_sprite = (self.animation_sprite + 1) % 4
                self.animation_tick = 0
                self.__update_sprite()

    def get_direction(self):
        return self.direction
    
    def set_direction(self, direction="right"):
        if self.direction != direction:
            self.direction = direction
            self.animation_sprite = 3
            self.animation_tick = self.ANIMATION_TICK - 1
        self.__advance_animation()

    def is_player_in_vision(self, player):
        return self.vision_service.is_target_in_vision(player)

    def is_ennemy_in_player_vision(self, player):
        # TODO : à changer pour la vision circulaire, actuellement on utilise un carré de 200px
        px, py = player.get_position()
        dx = self.x - px
        dy = self.y - py
        return dx**2 + dy**2 <= 200**2

    def draw_vision_cone(self, surface, camera):
        self.vision_service.draw_vision_cone(surface, camera)

    def draw_exclamation_mark(self, surface, camera):
        if self.alertness > 0:
            x = self.rect.centerx - self.image_exclamation_mark.get_width() / 2
            y = self.rect.top - self.image_exclamation_mark.get_height()
            surface.blit(self.image_exclamation_mark, (x + camera[0], y + camera[1]))

    def draw(self, surface, camera):
        self.draw_vision_cone(surface, camera)
        surface.blit(self.image, self.rect.move(camera))
        self.draw_exclamation_mark(surface, camera)

    def is_player_detected(self, player, clock):
        settings = Settings()
        if self.is_player_in_vision(player):
            self.guard_speed = self.GUARD_SPEED_ON_DETECT
            self.alertness += clock.tick(settings.FPS)
        else:
            self.alertness = 0
        return self.alertness >= self.DETECTION_TIME_MS

    def undo_move(self):
        self.x = self.prev_x
        self.y = self.prev_y
        self.rect.topleft = (self.x, self.y)

    def __get_current_patrol_step(self):
        return self.patrol_steps[self.current_step_index]

    def __move(self, dx, dy):
        self.x += dx * self.guard_speed
        self.y += dy * self.guard_speed

    """Begin paterne action def"""
    def __update_patrol_progress(self):
        self.step_progress += self.guard_speed

    def __patrol_step_finished(self):
        return (self.step_progress >= self.patrol_distance_x or
                self.step_progress >= self.patrol_distance_y)

    def __next_patrol_step(self):
        self.current_step_index = (self.current_step_index + 1) % len(self.patrol_steps)
        self.step_progress = 0
        self.patrol_distance_x = random.randint(self.x_range_min, self.x_range_max)
        self.patrol_distance_y = random.randint(self.y_range_min, self.y_range_max)
    """end paterne action def"""

    def __handle_collision(self, dungeon_map):
        offset = (dungeon_map.rect.x - self.rect.x, dungeon_map.rect.y - self.rect.y)
        if dungeon_map and self.mask.overlap(dungeon_map.dungeonMask, offset):
            self.undo_move()
            self.step_progress = self.patrol_distance_x

    def update(self, dungeon_map=None):
        self.prev_x = self.x
        self.prev_y = self.y

        step = self.__get_current_patrol_step()
        self.__move(step['dx'], step['dy'])
        self.set_direction(step['direction'])
        self.__update_patrol_progress()

        if self.__patrol_step_finished():
            self.__next_patrol_step()

        self.rect.topleft = (self.x, self.y)
        self.__handle_collision(dungeon_map)
        self.vision_service.update_cone_vision(self.rect, self.direction, dungeon_map)