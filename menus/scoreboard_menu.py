from typing import TypedDict

from components.composed_text import ComposedText
from components.medieval_button import MedievalButton
from components.medieval_panel import MedievalPanel
from components.medieval_text import MedievalText
from components.menu import Menu
from core.clock import Clock
from core.settings import Settings
from services.resources import Resources


class ScoreboardMenu:
    def __init__(self, screen_width: int, screen_height: int,
                 scores: list[TypedDict],
                 on_menu_action=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scores = scores

        self.resources = Resources()

        self.buttons = []

        # Panneau
        self.panel = MedievalPanel(
            self.resources.silver_panel_long_image,
            self.screen_width // 2,
            self.screen_height // 2
        )

        texts = []

        # Titre principal
        self.title = MedievalText(
            screen_width // 2, 140,
            "Tableau des scores",
            self.resources.title_font,
            Resources.LIGHT_SILVER_COLOR,
            shadow_offset=3
        )
        texts.append(self.title)

        # Textes des scores
        if self.scores:
            for i in range(10):
                score = None
                if i < len(self.scores):
                    score = self.scores[i]

                if i == 0:
                    color = Resources.GOLD_COLOR
                elif i == 1:
                    color = Resources.SILVER_COLOR
                elif i == 2:
                    color = Resources.WOOD_COLOR
                else:
                    color = Settings.WHITE

                first_text_center_y = 230
                offset_y = i % 5 * 80

                hour = ""
                minute = ""
                items = ""

                time_color = None
                if score:
                    hour = score["time"]["hour"]
                    minute = score["time"]["minute"]
                    items = score["items"]
                    time_color = Clock.get_clock_color(hour)

                first_text = MedievalText(
                    0, first_text_center_y + offset_y,
                    f"{i + 1}." if score else f"{i + 1}.",
                    self.resources.description_font,
                    color
                )
                if len(self.scores) > 5:
                    first_text.change_right_position(189 if i < 5 else 689)
                else:
                    first_text.change_right_position(449)

                if i < 5 or len(self.scores) > 5:
                    texts.append(ComposedText([first_text, *([
                        MedievalText(
                            0, first_text_center_y + offset_y,
                            f" Échappé à",
                            self.resources.description_font,
                            Settings.WHITE
                        ),
                        MedievalText(
                            0, first_text_center_y + offset_y,
                            f" {hour:02d}h{minute:02d} ",
                            self.resources.description_font,
                            time_color,
                        ),
                        MedievalText(
                            0, first_text_center_y + offset_y,
                            f"avec",
                            self.resources.description_font,
                            Settings.WHITE
                        ),
                        MedievalText(
                            0, first_text_center_y + offset_y,
                            f" {items} ",
                            self.resources.description_font,
                            Resources.WOOD_COLOR
                        ),
                         MedievalText(
                             0, first_text_center_y + offset_y,
                             f"items",
                             self.resources.description_font,
                             Settings.WHITE
                         )
                    ] if score else [])]))
        else:
            texts.append(MedievalText(
                screen_width // 2, screen_height // 2 - 45,
                "Aucun score encore enregistré.",
                self.resources.description_font,
                Resources.LIGHT_SILVER_COLOR
            ))
            texts.append(MedievalText(
                screen_width // 2, screen_height // 2,
                "Jouez une partie et échappez vous pour voir votre premier score",
                self.resources.description_font,
                Resources.LIGHT_SILVER_COLOR
            ))
            texts.append(MedievalText(
                screen_width // 2, screen_height // 2 + 45,
                "apparaître.",
                self.resources.description_font,
                Resources.LIGHT_SILVER_COLOR
            ))

        # Bouton retour menu
        self.menu_button = MedievalButton(
            200, 140, 0, 0,  # 890, 575
            on_menu_action,
            None, self.resources.gold_left_arrow_image,
            None, None,
            self.resources.gold_button_image_normal_square,
            self.resources.gold_button_image_pressed_square,
        )
        self.buttons.append(self.menu_button)

        # Créer le menu avec le composant générique
        self.menu = Menu(
            Resources.MENU_BACKGROUND_COLOR,
            self.panel,
            texts,
            self.buttons
        )

    def draw(self, surface):
        self.menu.draw(surface)
