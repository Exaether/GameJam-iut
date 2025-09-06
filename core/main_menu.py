from components import MedievalPanel
from components import MedievalText
from components import MedievalButton
from components import Menu
from components.animated_image import AnimatedImage
from services import Resources


class MainMenu:
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
            self.settings.MENU_SCREEN_WIDTH // 2,
            175,
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
            self.settings.MENU_SCREEN_WIDTH // 2 - 225,
            350, 0, 0,
            self.text_play,
            self.game.intro,
            None,
            None,
            self.resources.wood_button_image_normal,
            self.resources.wood_button_image_pressed
        )

        # Bouton crédits
        self.text_credits = MedievalText(
            0, 0, "Crédits",
            self.resources.button_font,
            self.resources.wood_color
        )
        self.button_credits = MedievalButton(
            self.settings.MENU_SCREEN_WIDTH // 2 - 225,
            450, 0, 0,
            self.text_credits,
            self.game.credits,
            None,
            None,
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
            self.settings.MENU_SCREEN_WIDTH // 2 - 225,
            550, 0, 0,
            self.text_exit,
            self.game.exit,
            None,
            None,
            self.resources.silver_button_image_normal_short,
            self.resources.silver_button_image_pressed_short
        )

        # Tutoriel
        self.tutorial = AnimatedImage([
            self.resources.tutorial_frame_00,
            self.resources.tutorial_frame_01,
            self.resources.tutorial_frame_02,
            self.resources.tutorial_frame_03,
            self.resources.tutorial_frame_04,
            self.resources.tutorial_frame_05,
            self.resources.tutorial_frame_06,
            self.resources.tutorial_frame_07,
            self.resources.tutorial_frame_08,
            self.resources.tutorial_frame_09,
            self.resources.tutorial_frame_10,
            self.resources.tutorial_frame_11,
            self.resources.tutorial_frame_12,
            self.resources.tutorial_frame_13,
            self.resources.tutorial_frame_14,
            self.resources.tutorial_frame_15
        ])
        self.tutorial_text_or = MedievalText(
            self.settings.MENU_SCREEN_WIDTH // 2 + 150,
            415,
            "OU",
            self.resources.button_font,
            self.resources.wood_color
        )

        # Créer le menu avec le composant générique
        self.menu_component = Menu(
            self.BACKGROUND_COLOR,
            self.panel,
            [self.game_text, self.tutorial_text_or],
            [self.button_play, self.button_credits, self.button_exit],
            self.tutorial,
            self.settings.MENU_SCREEN_WIDTH // 2 + 150,
            450
        )

    def update(self):
        self.menu_component.update()

    def draw(self, screen):
        self.menu_component.draw(screen)
