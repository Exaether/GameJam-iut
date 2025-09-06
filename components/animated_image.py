import pygame

from components.image import Image


class AnimatedImage:
    def __init__(self, frames: list[Image],
                 frame_delay=50, pause=1000):
        self.frames = frames
        self.frame_delay = frame_delay
        self.pause = pause
        self.index = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            if self.index == 0:
                if (now - self.last_update) > self.pause:
                    self.index = 1
                    self.last_update = now
            else:
                self.index = (self.index + 1) % len(self.frames)
                self.last_update = now

    def get_frame(self) -> Image:
        return self.frames[self.index]
