import pygame
from .medieval_text import MedievalText

class MedievalButton:
    NOBLE_BROWN = "#7D5B3A"
    RICH_HOVER = "#A0522D"
    ROYAL_GOLD = "#D9BF77"
    CRIMSON_BASE = "#A50034"
    CRIMSON_HOVER = "#C41E3A"
    DEEP_NAVY = "#2C3E50"
    DARK_GOLD = "#B8860B"
    ROYAL_BLUE = "#4682B4"
    BORDER_WIDTH = 3
    
    def __init__(self, center_x: int, center_y: int, width: int, height: int, 
                 text: MedievalText, base_color: str = None, hovering_color: str = None, on_click_action=None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.base_color = base_color if base_color else self.NOBLE_BROWN
        self.hovering_color = hovering_color if hovering_color else self.RICH_HOVER
        self.on_click_action = on_click_action

        self.rect = pygame.Rect((0, 0, self.width, self.height))
        self.rect.center = (self.center_x, self.center_y)
        
        self.text.center_x = self.center_x
        self.text.center_y = self.center_y
        self.text.text_rect = self.text.text_surf.get_rect(center=(self.center_x, self.center_y))
        self.text.shadow_rect = self.text.shadow_surf.get_rect(center=(self.center_x + self.text.shadow_offset, self.center_y + self.text.shadow_offset))

        self.is_hovering = False

    def draw(self, surface):
        # Couleur du bouton selon l'état (hover ou non)
        color = self.hovering_color if self.is_hovering else self.base_color
        
        # Dessin du bouton principal
        pygame.draw.rect(surface, color, self.rect)
        
        # Bordure
        pygame.draw.rect(surface, self.ROYAL_GOLD, self.rect, self.BORDER_WIDTH)
        
        # Bordure intérieure au hover
        if self.is_hovering:
            inner_rect = pygame.Rect(
                self.rect.x + 3, self.rect.y + 3,
                self.rect.width - 6, self.rect.height - 6
            )
            pygame.draw.rect(surface, self.DARK_GOLD, inner_rect, 1)

        # Texte par-dessus
        self.text.draw(surface)

    def check_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click_action:
            self.on_click_action()