import pygame

from core.credits import Credits
from core.intro_game import IntroGame
from core.playing import Playing
from core.settings import Settings
from core.state_manager import GameState
from menus.game_lose_menu import GameLoseMenu
from menus.game_win_menu import GameWinMenu
from menus.main_menu import MainMenu
from paths import get_asset_path


# Factory qui permet de créer les différents états du jeu
class StateFactory:
    def __init__(self, game):
        self.game = game

        self._registry = {
            GameState.INTRO: {
                "size": (Settings.GAME_SCREEN_WIDTH, Settings.GAME_SCREEN_HEIGHT),
                "music": "10-8bit10loop.ogg",
                "builder": lambda: IntroGame(self.game),
                # lambda permet d'encapsuler la création de l'objet, ce qui ne le crée que quand elle sera appellée
                "attr": "intro_scene",
                # Nom de l'attribut de la classe game dans lequel stocker l'objet créé
                "pre_process": None
            },
            GameState.PLAYING: {
                "size": (Settings.GAME_SCREEN_WIDTH, Settings.GAME_SCREEN_HEIGHT),
                "music": "10-8bit10loop.ogg",
                "builder": lambda: Playing(self.game, self.game.event_controller),
                "attr": "playing",
                "pre_process": self.game.event_controller.reset
            },
            GameState.CREDITS: {
                "size": (Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT),
                "music": "Mesmerizing Galaxy Loop.mp3",
                "builder": lambda: Credits(Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT),
                "attr": "credits_playing",
                "pre_process": None
            },
            GameState.LOSE: {
                "size": (Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: GameLoseMenu(Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT,
                                                self.game.retry_game, self.game.back_to_menu),
                "attr": "game_lose_menu",
                "pre_process": None
            },
            GameState.WIN: {
                "size": (Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: GameWinMenu(Settings.MENU_SCREEN_WIDTH,
                                               Settings.MENU_SCREEN_HEIGHT,
                                               self.game.playing.player.items_collected if self.game.playing else 0,
                                               self.game.playing.nb_items_max if self.game.playing else 0,
                                               self.game.retry_game, self.game.back_to_menu),
                "attr": "game_win_menu",
                "pre_process": None
            },
            GameState.MENU: {
                "size": (Settings.MENU_SCREEN_WIDTH, Settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: MainMenu(self.game),
                "attr": "menu",
                "pre_process": None
            }
        }

    def create(self, state: GameState):
        config = self._registry[state]

        # Changement de la taille de l'écran si elle est différente de celle actuelle
        if pygame.display.get_window_size() != config["size"]:
            self.game.screen = pygame.display.set_mode(config["size"])

        if config["pre_process"]:
            config["pre_process"]()

        # Création de l'instance de la classe
        instance = config["builder"]()
        setattr(self.game, config["attr"], instance)

        # On coupe la musique si on change d'état et l'active si l'état en possède une
        pygame.mixer.music.stop()
        if config["music"]:
            pygame.mixer.music.load(get_asset_path("music", config["music"]))
            pygame.mixer.music.play(-1)

        self.game.state_manager.change_state(state)
