from services.resources import Resources

from components.medieval_button import MedievalButton
from components.medieval_panel import MedievalPanel
from components.medieval_text import MedievalText
from components.menu import Menu


class GameWinMenu:

    def __init__(self, screen_width: int, screen_height: int, final_score: int, nb_items_max: int,
                 on_retry_action=None, on_menu_action=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        self.nb_items_max = nb_items_max

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
            screen_width // 2, 230,
            f"Trésors pillés : {final_score}",
            self.resources.subtitle_font,
            Resources.SILVER_COLOR
        )

        # Texte d'encouragement
        encouragement_message_1, encouragement_message_2, color = (
            GameWinMenu.__get_encouragement_message_and_color(final_score, nb_items_max)
        )
        if encouragement_message_2:
            self.encouragement_message_text_1 = MedievalText(
                screen_width // 2, 305,
                encouragement_message_1,
                self.resources.description_font,
                color
            )
            self.encouragement_message_text_2 = MedievalText(
                screen_width // 2, 340,
                encouragement_message_2,
                self.resources.description_font,
                color
            )
            texts = [self.title, self.score_text, self.encouragement_message_text_1, self.encouragement_message_text_2]
        else:
            self.encouragement_message_text_1 = MedievalText(
                screen_width // 2, 320,
                encouragement_message_1,
                self.resources.description_font,
                color
            )
            texts = [self.title, self.score_text, self.encouragement_message_text_1]

        # Bouton rejouer
        retry_text = MedievalText(
            0, 0, "Rejouer",
            self.resources.button_font, Resources.GOLD_COLOR
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 450, 0, 0,
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
            screen_width // 2, 545, 0, 0,
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
            texts,
            self.buttons
        )

    @staticmethod
    def __get_encouragement_message_and_color(nb_items_collected: int, nb_items_max: int):
        """Messages d'encouragement"""
        color = Resources.CRIMSON_COLOR
        if nb_items_collected <= 0:
            message_line_1 = "Qu'avez-vous fait ?"
            message_line_2 = ""
        elif nb_items_collected <= nb_items_max * 0.1:
            message_line_1 = "Hélas !"
            message_line_2 = "Les gardes étaient trop vigilants..."
            color = Resources.CRIMSON_COLOR
        elif nb_items_collected <= nb_items_max * 0.3:
            message_line_1 = "Quelques pièces d'or..."
            message_line_2 = "Un début prometteur !"
            color = Resources.WOOD_COLOR
        elif nb_items_collected <= nb_items_max * 0.6:
            message_line_1 = "Jolie butin !"
            message_line_2 = "Tu as volé plus que prévu !"
            color = Resources.PURPLE_COLOR
        elif nb_items_collected <= nb_items_max * 0.8:
            message_line_1 = "Belle razzia !"
            message_line_2 = "Tu deviens un habile brigand !"
            color = Resources.PURPLE_COLOR
        else:
            message_line_1 = "Magnifique butin !"
            message_line_2 = "Le roi tremble !"
            color = Resources.GOLD_COLOR
        return message_line_1, message_line_2, color

    def draw(self, surface):
        self.menu.draw(surface)
