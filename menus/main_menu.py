from components.animated_image import AnimatedImage
from components.medieval_button import MedievalButton
from components.medieval_panel import MedievalPanel
from components.medieval_text import MedievalText
from components.menu import Menu
from core.settings import Settings
from services.resources import Resources


class MainMenu:

    def __init__(self, game):
        self.game = game
        self.resources = Resources()

        self.buttons = []

        # Panneau
        self.panel = MedievalPanel(
            self.resources.wood_panel_image,
            Settings.MENU_SCREEN_WIDTH // 2,
            Settings.MENU_SCREEN_HEIGHT // 2
        )

        # Titre du jeu
        self.game_text = MedievalText(
            Settings.MENU_SCREEN_WIDTH // 2,
            175,
            Settings.GAME_TITLE,
            self.resources.title_font,
            Resources.LIGHT_WOOD_COLOR,
            shadow_offset=4
        )

        # Bouton jouer
        self.text_play = MedievalText(
            0, 0, "Jouer",
            self.resources.button_font,
            Resources.LIGHT_WOOD_COLOR
        )
        self.button_play = MedievalButton(
            Settings.MENU_SCREEN_WIDTH // 2 - 225,
            350, 0, 0,
            self.text_play,
            self.game.intro,
            None,
            None,
            self.resources.wood_button_image_normal,
            self.resources.wood_button_image_pressed
        )
        self.buttons.append(self.button_play)

        # Bouton crédits
        self.text_credits = MedievalText(
            0, 0, "Crédits",
            self.resources.button_font,
            Resources.LIGHT_WOOD_COLOR
        )
        self.button_credits = MedievalButton(
            Settings.MENU_SCREEN_WIDTH // 2 - 225,
            450, 0, 0,
            self.text_credits,
            self.game.credits,
            None,
            None,
            self.resources.wood_button_image_normal,
            self.resources.wood_button_image_pressed
        )
        self.buttons.append(self.button_credits)

        # Bouton quitter
        self.text_exit = MedievalText(
            0, 0, "Quitter",
            self.resources.button_font,
            Resources.CRIMSON_COLOR
        )
        self.button_exit = MedievalButton(
            Settings.MENU_SCREEN_WIDTH // 2 - 225,
            550, 0, 0,
            self.text_exit,
            self.game.exit,
            None,
            None,
            self.resources.silver_button_image_normal_short,
            self.resources.silver_button_image_pressed_short
        )
        self.buttons.append(self.button_exit)

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
            Settings.MENU_SCREEN_WIDTH // 2 + 150,
            415,
            "OU",
            self.resources.button_font,
            Resources.LIGHT_WOOD_COLOR
        )

        # Créer le menu avec le composant générique
        self.menu_component = Menu(
            Resources.MENU_BACKGROUND_COLOR,
            self.panel,
            [self.game_text, self.tutorial_text_or],
            self.buttons,
            self.tutorial,
            Settings.MENU_SCREEN_WIDTH // 2 + 150,
            450
        )

    def update(self):
        self.menu_component.update()

    def draw(self, screen):
        self.menu_component.draw(screen)
