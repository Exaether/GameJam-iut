from pygame.font import SysFont

from math import isclose
from time import time

from entities.enemy import Enemy
from entities.player import Player


class Clock:
    START_HOUR = 22
    START_MINUTE = 0
    SECONDS_PER_GAME_MINUTE = 1
    DAY_TIME_START = 7
    WARNING_TIME_START = 5
    BIG_WARNING_TIME_START = 6
    DAY_TIME_COLOR = (255, 255, 255)
    WARNING_TIME_COLOR = (255, 255, 0)
    BIG_WARNING_TIME_COLOR = (255, 165, 0)
    NIGHT_TIME_COLOR = (255, 0, 0)
    # Stat du joueur et des gardes en fonction de l'heure (ex: 5 = à partir de 5h00, 5.5 = à partir de 5h30...)
    # TODO: Ajoutez plus d'horaires ou pas
    HOURS_STAT = {
        22: {"player_vision": Player.VISION_RANGE, "enemy_vision_range": Enemy.VISION_RANGE,
             "enemy_vision_fov": Enemy.VISION_ANGLE, "enemy_speed": 2},
        5: {"player_vision": 205, "enemy_vision_range": 115, "enemy_vision_fov": 60, "enemy_speed": 2},
        5.5: {"player_vision": 210, "enemy_vision_range": 130, "enemy_vision_fov": 65, "enemy_speed": 2.5},
        6: {"player_vision": 215, "enemy_vision_range": 145, "enemy_vision_fov": 70, "enemy_speed": 3.5},
        6.5: {"player_vision": 220, "enemy_vision_range": 160, "enemy_vision_fov": 75, "enemy_speed": 5},
        8: {"player_vision": 220, "enemy_vision_range": 190, "enemy_vision_fov": 160, "enemy_speed": 5}
    }

    def __init__(self, screen_width):
        self.current_hour = self.START_HOUR
        self.current_minute = self.START_MINUTE

        self.seconds_per_game_minute = self.SECONDS_PER_GAME_MINUTE

        self.last_update_time = time()
        self.elapsed_seconds = 0

        self.font = SysFont("Arial", 48, bold=True)

        self.screen_width = screen_width

    def reset(self):
        self.current_hour = self.START_HOUR
        self.current_minute = self.START_MINUTE
        self.last_update_time = time()
        self.elapsed_seconds = 0

    def update(self, player, guards_list):
        now = time()
        delta = now - self.last_update_time
        self.last_update_time = now
        self.elapsed_seconds += delta

        while self.elapsed_seconds >= self.seconds_per_game_minute:
            self.elapsed_seconds -= self.seconds_per_game_minute
            self.current_minute += 1
            if self.current_minute >= 60:
                self.current_minute = 0
                self.current_hour += 1
                if self.current_hour >= 24:
                    self.current_hour = 0

        current_time = self.current_hour + self.current_minute / 60
        floating_point = current_time % 1

        if (isclose(floating_point, 0) or isclose(floating_point, 0.5)) and current_time in self.HOURS_STAT:
            Enemy.GUARD_DEFAULT_SPEED = self.HOURS_STAT[current_time]["enemy_speed"]
            player.vision_service.vision_range = self.HOURS_STAT[current_time]["player_vision"]
            for guard in guards_list:
                guard.vision_service.vision_range = self.HOURS_STAT[current_time]["enemy_vision_range"]
                guard.vision_service.vision_angle = self.HOURS_STAT[current_time]["enemy_vision_fov"]

    def draw(self, surface):
        if self.current_hour >= self.START_HOUR or self.current_hour < self.WARNING_TIME_START:
            color = self.DAY_TIME_COLOR
        elif self.WARNING_TIME_START <= self.current_hour < self.BIG_WARNING_TIME_START:
            color = self.WARNING_TIME_COLOR
        elif self.BIG_WARNING_TIME_START <= self.current_hour < self.DAY_TIME_START:
            color = self.BIG_WARNING_TIME_COLOR
        elif self.DAY_TIME_START <= self.current_hour < self.START_HOUR:
            color = self.NIGHT_TIME_COLOR
        else:
            color = self.DAY_TIME_COLOR
        time_str = f"{self.current_hour:02d}:{self.current_minute:02d}"
        text_surface = self.font.render(time_str, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.screen_width // 2, 10)
        surface.blit(text_surface, text_rect)
