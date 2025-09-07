from pygame.font import Font


class MedievalText:
    SHADOW_COLOR = "#2f1b14"

    def __init__(self, center_x: int, center_y: int, text: str,
                 font: Font, color: str, shadow_offset: int = 2):
        self.center_x = center_x
        self.center_y = center_y
        self.text = text
        self.font = font
        self.color = color
        self.shadow_offset = shadow_offset

        self.text_surf = self.font.render(text, True, self.color)
        self.shadow_surf = self.font.render(text, True, self.SHADOW_COLOR)

        self.text_rect = self.text_surf.get_rect(center=(self.center_x, self.center_y))
        self.shadow_rect = self.shadow_surf.get_rect(center=(
            self.center_x + shadow_offset,
            self.center_y + shadow_offset
        ))

    def draw(self, surface):
        """Dessine d'abord l'ombre puis le texte"""
        surface.blit(self.shadow_surf, self.shadow_rect)
        surface.blit(self.text_surf, self.text_rect)
