import pygame

from core.credits import Credits
from core.intro_game import IntroGame
from core.playing import Playing
from core.state_manager import GameState
from menus.game_lose_menu import GameLoseMenu
from menus.game_win_menu import GameWinMenu
from menus.main_menu import MainMenu
from paths import get_asset_path


# Factory qui permet de créer les différents états du jeu
class StateFactory:
    def __init__(self, game):
        self.game = game
        settings = game.settings
        self._registry = {
            GameState.INTRO: {
                "size": (settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT),
                "music": "10-8bit10loop.ogg",
                "builder": lambda: IntroGame(self.game),
                # lambda permet d'encapsuler la création de l'objet, ce qui ne le crée que quand elle sera appellée
                "attr": "intro_scene"
                # Nom de l'attribut de la classe game dans lequel stocker l'objet créé
            },
            GameState.PLAYING: {
                "size": (settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT),
                "music": "10-8bit10loop.ogg",
                "builder": lambda: Playing(self.game, self.game.event_controller),
                "attr": "playing"
            },
            GameState.CREDITS: {
                "size": (settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT),
                "music": "Mesmerizing Galaxy Loop.mp3",
                "builder": lambda: Credits(settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT),
                "attr": "credits_playing"
            },
            GameState.LOSE: {
                "size": (settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: GameLoseMenu(settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT,
                                                self.game.retry_game, self.game.back_to_menu),
                "attr": "game_lose_menu"
            },
            GameState.WIN: {
                "size": (settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: GameWinMenu(settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT,
                                               self.game.playing.player.items_collected if self.game.playing else 0,
                                               self.game.playing.nb_items_max if self.game.playing else 0,
                                               self.game.retry_game, self.game.back_to_menu),
                "attr": "game_win_menu"
            },
            GameState.MENU: {
                "size": (settings.MENU_SCREEN_WIDTH, settings.MENU_SCREEN_HEIGHT),
                "music": None,
                "builder": lambda: MainMenu(settings, self.game),
                "attr": "menu"
            }
        }

    def create(self, state: GameState):
        config = self._registry[state]

        # Changement de la taille de l'écran si elle est différente de celle actuelle
        if pygame.display.get_window_size() != config["size"]:
            self.game.screen = pygame.display.set_mode(config["size"])

        # Création de l'instance de la classe
        instance = config["builder"]()
        setattr(self.game, config["attr"], instance)

        # On coupe la musique si on change d'état et l'active si l'état en possède une
        pygame.mixer.music.stop()
        if config["music"]:
            pygame.mixer.music.load(get_asset_path("music", config["music"]))
            pygame.mixer.music.play(-1)

        self.game.state_manager.change_state(state)
