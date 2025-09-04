import pygame
from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_frame import MedievalFrame


class GameLoseScreen:
    TAVERN_BACKGROUND = "#2F1B14"

    def __init__(self, screen_width: int, screen_height: int,
                 on_retry_action=None, on_menu_action=None):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Cadre style parchemin
        frame_width = screen_width - 100
        frame_height = screen_height - 80
        self.main_frame = MedievalFrame(
            50, 40, frame_width, frame_height,
            border_width=6, shadow_offset=10
        )

        title_font = pygame.font.Font(None, 85)
        subtitle_font = pygame.font.Font(None, 55)
        button_font = pygame.font.Font(None, 42)

        # Titre principal en pourpre
        self.title = MedievalText(
            screen_width // 2, 140,
            "CAPTURÉ PAR LES GARDES !",
            title_font,
            MedievalText.CRIMSON_RED,
            shadow_offset=4
        )

        retry_text = MedievalText(
            screen_width // 2, 370, "NOUVELLE QUÊTE",
            button_font, MedievalText.PARCHMENT
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 370, 280, 75,
            retry_text,
            MedievalButton.DEEP_NAVY,
            MedievalButton.ROYAL_BLUE,
            on_retry_action
        )

        menu_text = MedievalText(
            screen_width // 2, 465, "RETOUR À LA TAVERNE",
            button_font, MedievalText.ROYAL_GOLD
        )
        self.menu_button = MedievalButton(
            screen_width // 2, 465, 320, 75,
            menu_text,
            MedievalButton.CRIMSON_BASE,
            MedievalButton.CRIMSON_HOVER,
            on_menu_action
        )

        self.buttons = [self.retry_button, self.menu_button]

    def draw(self, surface):
        surface.fill(self.TAVERN_BACKGROUND)

        # Cadre de parchemin
        self.main_frame.draw(surface)

        # Texte
        self.title.draw(surface)

        # Boutons
        for button in self.buttons:
            button.draw(surface)
