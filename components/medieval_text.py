from pygame.font import Font


class MedievalText:
    SHADOW_COLOR = "#2f1b14"

    def __init__(self, center_x: int, center_y: int, text: str,
                 font: Font, color: str, shadow_offset: int = 2):
        self.__center_x = center_x
        self.__center_y = center_y
        self.text = text
        self.font = font
        self.color = color
        self.shadow_offset = shadow_offset

        self.__text_surf = self.font.render(text, True, self.color)
        self.__shadow_surf = self.font.render(text, True, self.SHADOW_COLOR)

        self.__text_rect = self.__text_surf.get_rect(center=(self.__center_x, self.__center_y))
        self.__shadow_rect = self.__shadow_surf.get_rect(center=(
            self.__center_x + self.shadow_offset,
            self.__center_y + self.shadow_offset
        ))

    @property
    def get_rect(self):
        return self.__text_rect

    def change_position(self, center_x: int | None, center_y: int = None):
        """Non dynamique, à changer avant de dessiner"""
        if center_x:
            self.__center_x = center_x
            self.__text_rect.centerx = center_x
            self.__shadow_rect.centerx = center_x + self.shadow_offset
        if center_y:
            self.__center_y = center_y
            self.__text_rect.centery = center_y
            self.__shadow_rect.centery = center_y + self.shadow_offset

    def change_left_position(self, left: int):
        self.__center_x = left + self.__text_rect.width // 2
        self.__text_rect.left = left
        self.__shadow_rect.left = left + self.shadow_offset

    def change_right_position(self, right: int):
        self.__center_x = right - self.__text_rect.width // 2
        self.__text_rect.right = right
        self.__shadow_rect.right = right + self.shadow_offset

    def draw(self, surface):
        """Dessine d'abord l'ombre puis le texte"""
        surface.blit(self.__shadow_surf, self.__shadow_rect)
        surface.blit(self.__text_surf, self.__text_rect)
