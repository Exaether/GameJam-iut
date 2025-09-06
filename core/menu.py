from components import MedievalPanel
from components import MedievalText
from components import MedievalButton
from components import MenuComponent
from services import Resources



class Menu:
    BACKGROUND_COLOR = "#2F1B14"

    def __init__(self, settings, game):
        self.settings = settings
        self.game = game
        self.resources = Resources()

        # Panneau
        self.panel = MedievalPanel(
            self.resources.wood_panel_image,
            self.settings.MENU_SCREEN_WIDTH // 2,
            self.settings.MENU_SCREEN_HEIGHT // 2
        )

        # Titre du jeu
        self.game_text = MedievalText(
            self.settings.MENU_SCREEN_WIDTH // 2, 200,
            self.settings.GAME_TITLE,
            self.resources.title_font,
            self.resources.wood_color,
            shadow_offset=4
        )

        # Bouton jouer
        self.text_play = MedievalText(
            0, 0, "Jouer",
            self.resources.button_font,
            self.resources.wood_color
        )

        self.button_play = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2, 350, 0, 0,
            self.text_play,
            None,
            None,
            self.game.play,
            self.resources.wood_button_image_normal,
            self.resources.wood_button_image_pressed
        )

        # Bouton credit
        self.text_credit = MedievalText(
            0,0, "Credits",
            self.resources.button_font,
            self.resources.wood_color
        )
        self.button_credits = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2, 450, 0, 0,
            self.text_credit,
            None,
            None,
            self.game.credits,
            self.resources.wood_button_image_normal,
            self.resources.wood_button_image_pressed
        )

        # Bouton quitter
        self.text_exit = MedievalText(
            0, 0, "Quitter",
            self.resources.button_font,
            MedievalText.CRIMSON_RED
        )
        
        self.button_exit = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2, 550, 0, 0,
            self.text_exit,
            None,
            None,
            self.game.exit,
            self.resources.silver_button_image_normal_short,
            self.resources.silver_button_image_pressed_short
        )

        # Créer le menu avec le composant générique
        self.menu_component = MenuComponent(
            self.panel,
            self.game_text,
            [self.button_play, self.button_credits ,self.button_exit],
            self.BACKGROUND_COLOR
        )

    def draw(self, screen):
        self.menu_component.draw(screen)
