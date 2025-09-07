from services.resources import Resources

from components.medieval_button import MedievalButton
from components.medieval_panel import MedievalPanel
from components.medieval_text import MedievalText
from menus.menu import Menu


class GameLoseMenu:

    def __init__(self, screen_width: int, screen_height: int,
                 on_retry_action=None, on_menu_action=None):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.resources = Resources()

        # Panneau
        self.panel = MedievalPanel(
            self.resources.silver_panel_image,
            self.screen_width // 2,
            self.screen_height // 2
        )

        # Titre principal
        self.title_1 = MedievalText(
            screen_width // 2, 150,
            "Capturé",
            self.resources.title_font,
            Resources.CRIMSON_COLOR,
            shadow_offset=3
        )
        self.title_2 = MedievalText(
            screen_width // 2, 210,
            "par les gardes !",
            self.resources.title_font,
            Resources.CRIMSON_COLOR,
            shadow_offset=3
        )

        # Bouton rejouer
        retry_text = MedievalText(
            self.screen_width // 2, 370, "Rejouer",
            self.resources.button_font, Resources.SILVER_COLOR
        )
        self.retry_button = MedievalButton(
            screen_width // 2, 370, 0, 0,
            retry_text,
            on_retry_action,
            None,
            None,
            self.resources.silver_button_image_normal,
            self.resources.silver_button_image_pressed
        )

        # Bouton retour menu
        menu_text = MedievalText(
            screen_width // 2, 465, "Retour Menu",
            self.resources.button_font, Resources.SILVER_COLOR
        )
        self.menu_button = MedievalButton(
            screen_width // 2, 465, 0, 0,
            menu_text,
            on_menu_action,
            None,
            None,
            self.resources.silver_button_image_normal,
            self.resources.silver_button_image_pressed
        )

        self.buttons = [self.retry_button, self.menu_button]

        # Créer le menu avec le composant générique
        self.menu = Menu(
            Resources.MENU_BACKGROUND_COLOR,
            self.panel,
            [self.title_1, self.title_2],
            self.buttons
        )

    def draw(self, surface):
        self.menu.draw(surface)
