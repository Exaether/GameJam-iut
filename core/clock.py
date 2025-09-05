import pygame
import time

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
    

    def __init__(self, screen_width):
        self.current_hour = self.START_HOUR
        self.current_minute = self.START_MINUTE

        self.seconds_per_game_minute = self.SECONDS_PER_GAME_MINUTE

        self.last_update_time = time.time()
        self.elapsed_seconds = 0

        self.font = pygame.font.SysFont("Arial", 48, bold=True)

        self.screen_width = screen_width

    def reset(self):
        self.current_hour = self.START_HOUR
        self.current_minute = self.START_MINUTE
        self.last_update_time = time.time()
        self.elapsed_seconds = 0

    def update(self):
        now = time.time()
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

    def draw(self, surface):
        if (self.current_hour >= self.START_HOUR or self.current_hour < self.WARNING_TIME_START):
            color = (255, 255, 255)
        elif (self.current_hour >= self.WARNING_TIME_START and self.current_hour < self.BIG_WARNING_TIME_START):
            color = (255, 255, 0)
        elif (self.current_hour >= self.BIG_WARNING_TIME_START and self.current_hour < self.DAY_TIME_START):
            color = (255, 165, 0)
        elif (self.current_hour >= self.DAY_TIME_START and self.current_hour < self.START_HOUR):
            color = (255, 0, 0)
        else:
            color = (255, 255, 255) 
        time_str = f"{self.current_hour:02d}:{self.current_minute:02d}"
        text_surface = self.font.render(time_str, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.screen_width // 2, 10)
        surface.blit(text_surface, text_rect)
    