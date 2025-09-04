import pygame
from components import Button, Text, MenuComponent


class Menu:
    CENTER_Y_GAME_TEXT = 200

    @staticmethod
    def get_font_game_text() -> pygame.font.Font:
        return pygame.font.Font(None, 75)

    @staticmethod
    def get_font_buttons() -> pygame.font.Font:
        return pygame.font.Font(None, 40)

    WIDTH_BUTTONS = 250
    HEIGHT_BUTTONS = 80

    TEXT_BUTTON_PLAY = "VOLER !"
    CENTER_Y_PLAY_BUTTON = 400
    BASE_COLOR_PLAY_BUTTON = "#909090"
    HOVERING_COLOR_PLAY_BUTTON = "#707070"

    TEXT_BUTTON_EXIT = "FUIR"
    CENTER_Y_EXIT_BUTTON = 500
    BASE_COLOR_EXIT_BUTTON = "#ff0000"
    HOVERING_COLOR_EXIT_BUTTON = "#cc0000"

    BACKGROUND_COLOR = "#505050"

    def __init__(self, game):
        self.game = game
        self.game_text = Text(self.game.settings.SCREEN_WIDTH // 2, Menu.CENTER_Y_GAME_TEXT,
                              self.game.settings.GAME_TITLE, Menu.get_font_game_text())

        self.text_button_play = Text(0, 0, Menu.TEXT_BUTTON_PLAY, Menu.get_font_buttons())
        self.button_play = Button(self.game.settings.SCREEN_WIDTH // 2, Menu.CENTER_Y_PLAY_BUTTON, Menu.WIDTH_BUTTONS,
                                  Menu.HEIGHT_BUTTONS, self.text_button_play, Menu.BASE_COLOR_PLAY_BUTTON,
                                  Menu.HOVERING_COLOR_PLAY_BUTTON, None, self.game.play)

        self.text_button_exit = Text(0, 0, Menu.TEXT_BUTTON_EXIT, Menu.get_font_buttons())
        self.button_exit = Button(self.game.settings.SCREEN_WIDTH // 2, Menu.CENTER_Y_EXIT_BUTTON, Menu.WIDTH_BUTTONS,
                                  Menu.HEIGHT_BUTTONS, self.text_button_exit, Menu.BASE_COLOR_EXIT_BUTTON,
                                  Menu.HOVERING_COLOR_EXIT_BUTTON, None, self.game.exit)

        self.menu = MenuComponent(self.game_text, [self.button_play, self.button_exit], Menu.BACKGROUND_COLOR)

    def draw(self, screen):
        self.menu.draw(screen)
