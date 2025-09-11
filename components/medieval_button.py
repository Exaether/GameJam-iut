import pygame

from components.image import Image
from components.medieval_text import MedievalText
from services.resources import Resources


class MedievalButton:
    BORDER_WIDTH = 3

    def __init__(self, center_x: int, center_y: int, width: int, height: int, on_click_action,
                 text: MedievalText | None, image: Image | None,
                 base_background_color: str | None, hovering_background_color: str = None,
                 base_background_image: Image = None, hovering_background_image: Image = None):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.base_background_color = base_background_color
        self.hovering_background_color = hovering_background_color
        self.base_background_image = base_background_image
        self.hovering_background_image = hovering_background_image
        self.on_click_action = on_click_action

        if image:
            self.image_rect = image.image_surf.get_rect(centerx=center_x)

        if base_background_image:
            self.rect = self.base_background_image.image_surf.get_rect(center=(self.center_x, self.center_y))
        else:
            self.rect = pygame.Rect((0, 0, self.width, self.height))
            self.rect.center = (self.center_x, self.center_y)

        if self.text:
            self.text.change_position(self.center_x)

        self.is_hovering = False

        # Vérifie si le bouton est survolé à sa création (sans aucun évènement)
        self.check_hover(pygame.mouse.get_pos())

    def draw(self, surface):
        # Si pas d'image de fond
        if not self.base_background_image:
            # Couleur de fond du bouton selon l'état (hover ou non)
            color = self.hovering_background_color if self.is_hovering else self.base_background_color

            # Dessin de la couleur de fond
            pygame.draw.rect(surface, color, self.rect)

            # Bordure
            pygame.draw.rect(surface, Resources.LIGHT_GOLD_COLOR, self.rect, self.BORDER_WIDTH)

            # Bordure intérieure au hover
            if self.is_hovering:
                inner_rect = pygame.Rect(
                    self.rect.x + 3, self.rect.y + 3,
                    self.rect.width - 6, self.rect.height - 6
                )
                pygame.draw.rect(surface, Resources.LIGHT_GOLD_COLOR, inner_rect, 1)
        else:
            # Image de fond selon l'état (survolé ou non) et si une image de fond de survol est définie
            if self.hovering_background_image and self.is_hovering:
                background_image = self.hovering_background_image
                # Descend le texte ou l'image pour l'adapter au bouton pressé
                if self.text:
                    self.text.change_position(None, self.center_y - 3)
                if self.image:
                    self.image_rect.centery = self.center_y
            else:
                background_image = self.base_background_image
                # Remonte le texte ou l'image pour l'adapter au bouton non pressé
                if self.text:
                    self.text.change_position(None, self.center_y - 7)
                if self.image:
                    self.image_rect.centery = self.center_y - 5

            # Dessin de l'image de fond
            surface.blit(background_image.image_surf, self.rect)

        # Dessin du texte ou de l'image
        if self.text:
            self.text.draw(surface)
        if self.image:
            surface.blit(self.image.image_surf, self.image_rect)

    def check_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click_action:
            self.on_click_action()
