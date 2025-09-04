import pygame

class MedievalFrame:
    PARCHMENT_BASE = "#E9C7A5"   
    PARCHMENT_DARK = "#D3BA9C"
    ROYAL_GOLD = "#D9BF77"
    NOBLE_BRONZE = "#CD853F"
    DEEP_SHADOW = "#5E3B49"
    RICH_BROWN = "#7D5B3A"
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 border_width: int = 5, shadow_offset: int = 6):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_width = border_width
        self.shadow_offset = shadow_offset
        
        # Rectangles pour les différents effets de profondeur
        self.shadow_rect = pygame.Rect(
            x + shadow_offset, y + shadow_offset, 
            width, height
        )
        # Rectangle pour le contenu
        self.inner_rect = pygame.Rect(
            x + border_width, y + border_width,
            width - (border_width * 2), height - (border_width * 2)
        )
        # Rectangle pour texture parchemin
        self.texture_rect = pygame.Rect(
            x + border_width + 2, y + border_width + 2,
            width - (border_width + 2) * 2, height - (border_width + 2) * 2
        )
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.DEEP_SHADOW, self.shadow_rect)
        
        pygame.draw.rect(surface, self.PARCHMENT_BASE, self.rect)
        pygame.draw.rect(surface, self.PARCHMENT_DARK, self.texture_rect)
        
        pygame.draw.rect(surface, self.ROYAL_GOLD, self.rect, self.border_width)
        
        if self.border_width > 3:
            pygame.draw.rect(surface, self.NOBLE_BRONZE, self.inner_rect, 2)
        