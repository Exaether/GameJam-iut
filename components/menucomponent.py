import pygame
from .text import Text
from .button import Button


class MenuComponent:
    def __init__(self, text: Text, buttons: list[Button], background_color):
        self.text = text
        self.buttons = buttons
        self.background_color = background_color

    def draw(self, screen):
        screen.fill(self.background_color)
        self.text.draw(screen)
        for button in self.buttons:
            button.draw(screen)
