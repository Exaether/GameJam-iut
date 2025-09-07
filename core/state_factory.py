import pygame
from paths import get_asset_path

from core.state_manager import GameState
from core.playing import Playing
from core.intro_game import IntroGame
from core.credits import Credits
from menus.game_lose_menu import GameLoseMenu
from menus.game_win_menu import GameWinMenu

# Factory qui permet de créer les différent état du jeu
class StateFactory:
    def __init__(self, game):
        self.game = game
        settings = game.settings
        self._registry = {
            GameState.INTRO: {
                "size": (settings.GAME_SCREEN_WIDTH, settings.GAME_SCREEN_HEIGHT),
                "music": "10-8bit10loop.ogg",
                "builder": lambda: IntroGame(self.game), # lambda permet de pas créer la classe quand on veut (et non tout de suite ce qui ferait planter le jeu)
                "attr": "intro_scene" # attribut de la class game, comme pas def (car classe générique) on l'écrit en brute
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
                "builder": lambda: self.game.menu, # déjà créé dans le game, juste on l'appelle (lambda ici permet une reutilisation)
                "attr": "menu"
            }
        }

    def create(self, state: GameState):
        config = self._registry[state]

        # config de la taille de l'écran
        self.game.screen = pygame.display.set_mode(config["size"])

        # création ou récupération de l'instance de la classe
        instance = config["builder"]()
        setattr(self.game, config["attr"], instance)

        # On coupe la musique si on change d'état et l'active si l'état en possède une
        pygame.mixer.music.stop()
        if config["music"]:
            pygame.mixer.music.load(get_asset_path("music", config["music"]))
            pygame.mixer.music.play(-1)

        # changer l'état
        self.game.state_manager.change_state(state)
