import pygame


class Text:
    TEXT_COLOR = "#000000"

    def __init__(self, center_x: int, center_y: int, text: str, font: pygame.font.Font):
        self.center_x = center_x
        self.center_y = center_y
        self.text = text
        self.font = font

        self.text_surf = self.font.render(text, True, Text.TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=(self.center_x, self.center_y))

    def draw(self, surface):
        surface.blit(self.text_surf, self.text_rect)
