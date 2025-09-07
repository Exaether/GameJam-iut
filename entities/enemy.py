import pygame

from random import randint
from paths import get_asset_path

from services.resources import Resources
from services.vision_service import VisionService

from core.settings import Settings


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
    VALID_DIRECTIONS = ["left", "right", "up", "down"]

    def __init__(self, x_start=0, y_start=0, x_range_min=0, x_range_max=0, y_range_min=0, y_range_max=0,
                 pattern_type_def="square", direction_def="right"):
        super().__init__()
        self.__init_sprite(pattern_type=pattern_type_def, direction=direction_def)
        self.__init_position(x_start, y_start)
        self.__init_patrol_ranges(x_range_min, x_range_max, y_range_min, y_range_max)
        self.__init_patrol_steps(pattern_type_def, direction_def)
        self.__init_alertness()
        self.__init_collision()
        self.vision_service = VisionService(self.VISION_RANGE, self.VISION_ANGLE)
        self.speed_multiplier = 1.0

    def __init_sprite(self, pattern_type="square", direction = "right"):
        sprite_path = get_asset_path("entities", "enemy_sprite.png")
        self.sprite_sheet = pygame.image.load(sprite_path)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.SPRITE_SIZE * 4, self.SPRITE_SIZE * 2))
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.__get_image()
        self.rect = self.image.get_rect()
        self.direction = direction
        if direction not in self.VALID_DIRECTIONS:
            raise ValueError(f"Invalid direction '{direction}' for Enemy")
        self.animation_tick = 0
        self.animation_sprite = 0
        self.guard_speed = self.GUARD_DEFAULT_SPEED
        self.pattern_type = pattern_type  # type possible : ["fixe","square"]
        self.last_detect_sound_time = 0

    def __init_position(self, x, y):
        self.x = x
        self.y = y

    def __init_patrol_ranges(self, x_min, x_max, y_min, y_max):
        self.x_range_min = x_min
        self.x_range_max = x_max
        self.y_range_min = y_min
        self.y_range_max = y_max
        self.patrol_distance_x = 0
        self.patrol_distance_y = 0

    def __init_patrol_steps(self, pattern_type, direction="right"):
        if pattern_type == "square" or pattern_type == "fixe":
            self.patrol_steps = [
                {'direction': 'right', 'dx': 1, 'dy': 0},
                {'direction': 'down', 'dx': 0, 'dy': 1},
                {'direction': 'left', 'dx': -1, 'dy': 0},
                {'direction': 'up', 'dx': 0, 'dy': -1}
            ]
        else:
            raise ValueError(
                f"Pattern type {pattern_type} not supported")

        match direction:
            case "right":
                self.current_step_index = 0
                if self.x_range_min > 0:
                    self.x_range_min = self.x_range_min * (-1)
                if self.x_range_max > 0:
                    self.x_range_max = self.x_range_max * (-1)
            case "down":
                self.current_step_index = 1
                if self.y_range_min < 0:
                    self.y_range_min = self.y_range_min * (-1)
                if self.y_range_max < 0:
                    self.y_range_max = self.y_range_max * (-1)
            case "left":
                self.current_step_index = 2
                if self.x_range_min > 0:
                    self.x_range_min = self.x_range_min * (-1)
                if self.x_range_max > 0:
                    self.x_range_max = self.x_range_max * (-1)
            case "up":
                self.current_step_index = 3
                if self.x_range_min > 0:
                    self.x_range_min = self.x_range_min * (-1)
                if self.x_range_max > 0:
                    self.x_range_max = self.x_range_max * (-1)
        self.step_progress = 0

    def __init_alertness(self):
        self.alertness = 0
        exclamation_path = get_asset_path("other", "exclamation_mark.png")
        self.exclamation_mark = pygame.image.load(exclamation_path)
        self.exclamation_mark = pygame.transform.scale(self.exclamation_mark,
                                                       (self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK))
        self.image_exclamation_mark = pygame.Surface([self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK])
        self.image_exclamation_mark.blit(self.exclamation_mark, (0, 0),
                                         (0, 0, self.SIZE_EXCLAMATION_MARK, self.SIZE_EXCLAMATION_MARK))
        self.image_exclamation_mark.set_colorkey([0, 0, 0])

    def __init_collision(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.mask = pygame.mask.Mask((self.SPRITE_SIZE, self.SPRITE_SIZE), True)

    def __get_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0, 0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    def __get_sprite_y(self):
        if self.direction in ("right", "down"):
            sprite_y = 0
        else:
            sprite_y = self.SPRITE_SIZE
        return sprite_y

    def __get_sprite_x(self):
        return self.SPRITE_SIZE * self.animation_sprite

    def __update_sprite(self):
        """Mise à jour de l'emplacement du sprite"""
        self.__get_image(self.__get_sprite_x(), self.__get_sprite_y())

    def __update_animation(self):
        """Anime suivant le nombre de tick le déplacement du garde"""
        if self.pattern_type == "square":
            self.animation_tick += 1
            if self.animation_tick == self.ANIMATION_TICK:
                self.animation_sprite = (self.animation_sprite + 1) % 4
                self.animation_tick = 0
                self.__update_sprite()

    def set_direction(self, direction="right"):
        """modifie le sprite suivant la direction"""
        if self.direction != direction:
            self.direction = direction
            self.animation_sprite = 3
            self.animation_tick = self.ANIMATION_TICK - 1
        self.__update_animation()

    def apply_vision_scale(self, range_multiplier=1.0, angle_multiplier=1.0):
        self.vision_service.vision_range = int(self.vision_service.vision_range * range_multiplier)
        self.vision_service.vision_angle_degree = int(self.vision_service.vision_angle_degree * angle_multiplier)

    def is_player_in_vision(self, player):
        """Informe si le garde voit le joueur """
        return self.vision_service.is_target_in_vision(player)

    def is_enemy_in_player_vision(self, player):
        return player.vision_service.is_target_in_vision(self)

    def draw_vision_cone(self, surface, camera):
        self.vision_service.draw_vision_cone(surface, camera)

    def draw_exclamation_mark(self, surface, camera):
        """Dessine un '!' au-dessus du sprite (souvant utilisé en cas de détection de joueur)"""
        if self.alertness > 0:
            x = self.rect.centerx - self.image_exclamation_mark.get_width() / 2
            y = self.rect.top - self.image_exclamation_mark.get_height()
            surface.blit(self.image_exclamation_mark, (x + camera[0], y + camera[1]))

    def draw(self, surface, camera):
        self.draw_vision_cone(surface, camera)
        surface.blit(self.image, self.rect.move(camera))
        self.draw_exclamation_mark(surface, camera)

    def is_player_detected(self, player, clock):
        """Si un joueur est détecté, le gard va à la même vitesse que lui grâce à la constante GUARD_SPEED_ON_DETECT"""
        settings = Settings()
        if self.is_player_in_vision(player):
            self.guard_speed = self.GUARD_SPEED_ON_DETECT * self.speed_multiplier
            self.alertness += clock.tick(settings.FPS)
            if pygame.time.get_ticks() - self.last_detect_sound_time >= 1000:  # 1 seconde
                Resources().detect_sound.play()
                self.last_detect_sound_time = pygame.time.get_ticks()
        else:
            self.alertness = 0

            self.guard_speed = self.GUARD_DEFAULT_SPEED * self.speed_multiplier
        return self.alertness >= self.DETECTION_TIME_MS

    def undo_move(self):
        """Annule un mouvement (souvent utilisé suite à un contact sur une collision)"""
        self.x = self.prev_x
        self.y = self.prev_y
        self.rect.topleft = (self.x, self.y)
        self.__next_patrol_step()

    def __get_current_patrol_step(self):
        return self.patrol_steps[self.current_step_index]

    def __move(self, dx, dy):
        if dx != 0:
            self.x += dx * self.guard_speed
        if dy != 0:
            self.y += dy * self.guard_speed

    def __update_patrol_progress(self):
        """Agmente la progression du parcours de 1 par pixel parcouru utilisé dans __patrol_step_finished("""
        self.step_progress += self.guard_speed

    def __patrol_step_finished(self):
        """Signale si le garde a parcouru la distance de son parcours aléatoire"""
        first_flag = False
        second_flag = False
        if self.x_range_max > 0:
            first_flag = self.step_progress >= self.patrol_distance_x
        if self.y_range_max > 0:
            second_flag = self.step_progress >= self.patrol_distance_y
        return first_flag or second_flag

    def __next_patrol_step(self):
        """Modifie la direction vers l'opposer"""
        match self.current_step_index:
            case 0:
                self.current_step_index = 2
            case 1:
                self.current_step_index = 3
            case 2:
                self.current_step_index = 0
            case 3:
                self.current_step_index = 1
        self.step_progress = 0
        self.patrol_distance()

    def __handle_collision(self, dungeon_map):
        """Détection des murs ou objet bloquant"""
        offset = (dungeon_map.rect.x - self.rect.x, dungeon_map.rect.y - self.rect.y)
        if dungeon_map and self.mask.overlap(dungeon_map.dungeonMask, offset):
            self.undo_move()
            self.step_progress = self.patrol_distance_x

    def patrol_distance(self):
        """Distance de déplacement des choses aléatoirement entre x_minimum et x_maximum ou y """
        self.x_range_min, self.x_range_max = sorted([self.x_range_min, self.x_range_max])
        self.y_range_min, self.y_range_max = sorted([self.y_range_min, self.y_range_max])
        self.patrol_distance_x = randint(self.x_range_min, self.x_range_max)
        self.patrol_distance_y = randint(self.y_range_min, self.y_range_max)

    def update(self, dungeon_map=None):
        self.prev_x = self.x
        self.prev_y = self.y

        if self.pattern_type == "square":
            step = self.__get_current_patrol_step()
            self.__move(step['dx'], step['dy'])
            self.set_direction(step['direction'])
            self.__update_patrol_progress()

        if self.pattern_type == "fixe" and self.direction == "left" or self.direction == "down":
            self.__get_image(0, self.SPRITE_SIZE)

        if self.__patrol_step_finished():
            self.__next_patrol_step()

        self.rect.topleft = (self.x, self.y)
        self.__handle_collision(dungeon_map)
        self.vision_service.update_cone_vision(self.rect, self.direction, dungeon_map)
