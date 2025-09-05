import pygame

from services import Resources
from .medieval_text import MedievalText
from .medieval_button import MedievalButton
from .medieval_panel import MedievalPanel


class GameWinScreen:
    TAVERN_BACKGROUND = "#2F1B14"

    def __init__(self, screen_width: int, screen_height: int, final_score: int,
                 on_retry_action=None, on_menu_action=None):
        self.settings = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        self.resources = Resources()

        # Panneau
        self.panel = MedievalPanel(
            self.resources.gold_panel_image,
            self.screen_width // 2,
            self.screen_height // 2
        )

        # Titre principal en bronze
        self.title = MedievalText(
            screen_width // 2, 140,
            "Vous vous etes echappes !",
            self.resources.title_font,
            MedievalText.FOREST_GREEN,
            shadow_offset=4
        )

        # Sous-titre
        self.score_text = MedievalText(
            screen_width // 2, 210,
            f"Tresors pilles : {final_score}",
            self.resources.subtitle_font,
            MedievalText.ROYAL_GOLD
        )

        encouragement_message = GameWinScreen.__get_encouragement_message(final_score)
        self.encouragement_message_text = MedievalText(
            screen_width // 2, 270,
            encouragement_message,
            self.resources.description_font,
            MedievalText.NOBLE_BRONZE
        )

        retry_text = MedievalText(
            screen_width // 2, 370, "NOUVELLE QUETE",
            self.resources.button_font, self.resources.gold_color
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 370, 0, 0,
            retry_text,
            None,
            None,
            on_retry_action,
            self.resources.gold_button_image_normal,
            self.resources.gold_button_image_pressed
        )

        menu_text = MedievalText(
            screen_width // 2, 465, "TAVERNE",
            self.resources.button_font, self.resources.gold_color
        )
        self.menu_button = MedievalButton(
            screen_width // 2, 465, 0, 0,
            menu_text,
            None,
            None,
            on_menu_action,
            self.resources.gold_button_image_normal,
            self.resources.gold_button_image_pressed
        )

        self.buttons = [self.retry_button, self.menu_button]

    @staticmethod
    def __get_encouragement_message(score: int) -> str:
        """Messages d'encouragement dans le style médiéval noble"""
        if score == 0:
            return "Helas ! Les gardes etaient trop vigilants..."
        elif score <= 3:
            return "Quelques pieces d'or... Un debut prometteur !"
        elif score <= 7:
            return "Belle razzia ! Tu deviens un habile brigand !"
        else:
            return "Magnifique butin ! Le roi tremble !"

    def draw(self, surface):
        surface.fill(self.TAVERN_BACKGROUND)

        self.panel.draw(surface)
        self.title.draw(surface)
        self.score_text.draw(surface)
        self.encouragement_message_text.draw(surface)

        for button in self.buttons:
            button.draw(surface)
