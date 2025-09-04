import pygame
from .text import Text


class Button:
    def __init__(self, center_x: int, center_y: int, width: int, height: int, text: Text, base_color,
                 hovering_color, image, on_click_action):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.image = image
        self.on_click_action = on_click_action

        if image:
            self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
        else:
            self.rect = pygame.Rect((0, 0, self.width, self.height))
            self.rect.center = (self.center_x, self.center_y)
        text.text_rect = text.text_surf.get_rect(center=self.rect.center)

        self.is_hovering = False

    def draw(self, surface):
        color = self.hovering_color if self.is_hovering else self.base_color
        pygame.draw.rect(surface, color, self.rect)

        self.text.draw(surface)

    def __on_click(self):
        if self.is_hovering:
            self.on_click_action()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovering = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__on_click()
