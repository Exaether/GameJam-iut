from services.resources import Resources

from components.medieval_button import MedievalButton
from components.medieval_panel import MedievalPanel
from components.medieval_text import MedievalText
from components.menu import Menu


class GameWinMenu:

    def __init__(self, screen_width: int, screen_height: int, final_score: int,
                 on_retry_action=None, on_menu_action=None):
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

        # Titre principal
        self.title = MedievalText(
            screen_width // 2, 150,
            "Vous avez fui !",
            self.resources.title_font,
            Resources.GOLD_COLOR,
            shadow_offset=3
        )

        # Sous-titre
        self.score_text = MedievalText(
            screen_width // 2, 225,
            f"Trésors pillés : {final_score}",
            self.resources.subtitle_font,
            Resources.SILVER_COLOR
        )

        encouragement_message = GameWinMenu.__get_encouragement_message(final_score)
        self.encouragement_message_text = MedievalText(
            screen_width // 2, 290,
            encouragement_message,
            self.resources.description_font,
            Resources.PURPLE_COLOR
        )

        # Bouton rejouer
        retry_text = MedievalText(
            0, 0, "Rejouer",
            self.resources.button_font, Resources.GOLD_COLOR
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 400, 0, 0,
            retry_text,
            on_retry_action,
            None,
            None,
            self.resources.gold_button_image_normal,
            self.resources.gold_button_image_pressed
        )

        # Bouton retour menu
        menu_text = MedievalText(
            0, 0, "Retour Menu",
            self.resources.button_font, Resources.GOLD_COLOR
        )
        self.menu_button = MedievalButton(
            screen_width // 2, 495, 0, 0,
            menu_text,
            on_menu_action,
            None,
            None,
            self.resources.gold_button_image_normal,
            self.resources.gold_button_image_pressed
        )

        self.buttons = [self.retry_button, self.menu_button]

        # Créer le menu avec le composant générique
        self.menu = Menu(
            Resources.MENU_BACKGROUND_COLOR,
            self.panel,
            [self.title, self.score_text, self.encouragement_message_text],
            self.buttons
        )

    @staticmethod
    def __get_encouragement_message(score: int) -> str:
        """Messages d'encouragement dans le style médiéval noble"""
        if score == 0:
            return "Hélas ! Les gardes étaient trop vigilants..."
        elif score <= 3:
            return "Quelques pièces d'or... Un début prometteur !"
        elif score <= 7:
            return "Belle razzia ! Tu deviens un habile brigand !"
        else:
            return "Magnifique butin ! Le roi tremble !"

    def draw(self, surface):
        self.menu.draw(surface)
