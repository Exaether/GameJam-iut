from pygame import Rect
from pygame.draw import rect
from pygame.mouse import get_pos

from components.image import Image
from components.medieval_text import MedievalText
from services.resources import Resources


class MedievalButton:
    BORDER_WIDTH = 3

    def __init__(self, center_x: int, center_y: int, width: int, height: int, text: MedievalText,
                 on_click_action, base_color: str | None, hovering_color: str = None,
                 base_image: Image = None, hovering_image: Image = None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.base_image = base_image
        self.hovering_image = hovering_image
        self.on_click_action = on_click_action

        if base_image:
            self.rect = self.base_image.image_surf.get_rect(center=(self.center_x, self.center_y))
        else:
            self.rect = Rect((0, 0, self.width, self.height))
            self.rect.center = (self.center_x, self.center_y)

        self.text.change_position(self.center_x, self.center_y - 7)

        self.is_hovering = False

        # Vérifie si le bouton est survolé à sa création (sans aucun évènement)
        self.check_hover(get_pos())

    def draw(self, surface):
        # Si pas d'image
        if not self.base_image:
            # Couleur du bouton selon l'état (hover ou non)
            color = self.hovering_color if self.is_hovering else self.base_color

            # Dessin du bouton principal
            rect(surface, color, self.rect)

            # Bordure
            rect(surface, Resources.LIGHT_GOLD_COLOR, self.rect, self.BORDER_WIDTH)

            # Bordure intérieure au hover
            if self.is_hovering:
                inner_rect = Rect(
                    self.rect.x + 3, self.rect.y + 3,
                    self.rect.width - 6, self.rect.height - 6
                )
                rect(surface, Resources.LIGHT_GOLD_COLOR, inner_rect, 1)
        else:
            # Image selon l'état (survolé ou non) et si une image de survol est définie
            if self.hovering_image and self.is_hovering:
                image = self.hovering_image
                # Descend le texte pour l'adapter au bouton pressé
                self.text.change_position(self.center_x, self.center_y - 3)
            else:
                image = self.base_image
                # Remonte le texte pour l'adapter au bouton non pressé
                self.text.change_position(self.center_x, self.center_y - 7)

            # Dessin de l'image
            surface.blit(image.image_surf, self.rect)

        # Texte par-dessus
        self.text.draw(surface)

    def check_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click_action:
            self.on_click_action()
