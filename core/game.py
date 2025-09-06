import pygame

from sys import exit
from os import environ

from core.game_lose_menu import GameLoseMenu
from core.game_win_menu import GameWinMenu
from core.main_menu import MainMenu
from core.settings import Settings
from core.state_manager import StateManager, GameState
from core.event_controller import EventController
from core.playing import Playing
from core.credits import Credits
from core.intro_game import IntroGame

class Game:
    def __init__(self):
        pygame.init()

        # Centre la fênetre de jeu sur le bureau
        environ['SDL_VIDEO_CENTERED'] = "true"

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        self.menu = MainMenu(self.settings, self)

        self.playing = Playing(self, self.event_controller)
        self.intro_scene = None
        self.running = True

        self.game_lose_menu = None
        self.game_win_menu = None

    def intro(self):
        self.screen = pygame.display.set_mode((self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT))
        self.intro_scene = IntroGame(self)
        self.state_manager.change_state(GameState.INTRO)
        pygame.mixer.music.load('./assets/music/10-8bit10loop.ogg')
        pygame.mixer.music.play(-1)

    def credits(self):
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.credits_playing = Credits(self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT)
        self.state_manager.change_state(GameState.CREDITS)
        pygame.mixer.music.load("./assets/music/Mesmerizing Galaxy Loop.mp3")
        pygame.mixer.music.play(-1)

    def play(self):
        self.screen = pygame.display.set_mode((self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT))
        self.playing = Playing(self, self.event_controller)
        pygame.mixer.music.load('./assets/music/10-8bit10loop.ogg')
        pygame.mixer.music.play(-1)
        self.state_manager.change_state(GameState.PLAYING)

    def retry_game(self):
        """Relance une nouvelle partie"""
        self.game_lose_menu = None
        self.game_win_menu = None
        self.screen = pygame.display.set_mode((self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT))
        self.play()

    def back_to_menu(self):
        """Retourne au menu principal"""
        self.game_lose_menu = None
        self.game_win_menu = None
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.state_manager.change_state(GameState.MENU)

    def trigger_game_lose(self):
        """Déclenche la défaite du jeu"""
        self.game_lose_menu = GameLoseMenu(
            self.settings.MENU_SCREEN_WIDTH,
            self.settings.MENU_SCREEN_HEIGHT,
            self.retry_game,
            self.back_to_menu
        )
        self.playing = Playing(self, self.event_controller)
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.state_manager.change_state(GameState.LOSE)
        pygame.mixer.music.stop()

    def trigger_game_win(self):
        """Déclenche la victoire du jeu"""
        final_score = self.playing.player.items_collected
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.game_win_menu = GameWinMenu(
            self.settings.MENU_SCREEN_WIDTH,
            self.settings.MENU_SCREEN_HEIGHT,
            final_score,
            self.retry_game,
            self.back_to_menu
        )
        self.playing = Playing(self, self.event_controller)
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.state_manager.change_state(GameState.WIN)
        pygame.mixer.music.stop()

    def exit(self):
        self.running = False

    def run(self):
        while self.running:
            events = pygame.event.get()
            dt = self.clock.tick(self.settings.FPS) / 1000

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.event_controller.handle_events(events, dt)

            current_state = self.state_manager.get_current_state()

            if current_state == GameState.PLAYING:
                self.playing.update(dt)
                self.playing.draw(self.screen)
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
            elif current_state == GameState.PAUSED:
                # TODO: A réaliser
                pass
            elif current_state == GameState.MENU:
                self.menu.update()
                self.menu.draw(self.screen)
            elif current_state == GameState.LOSE:
                if self.game_lose_menu:
                    pygame.mixer.music.stop()
                    self.game_lose_menu.draw(self.screen)
                else:
                    # Initialiser l'écran Game Lose à la première image
                    self.trigger_game_lose()
            elif current_state == GameState.WIN:
                if self.game_win_menu:
                    pygame.mixer.music.stop()
                    self.game_win_menu.draw(self.screen)
                else:
                    # Initialiser l'écran Game Win à la première image
                    self.trigger_game_win()
            elif current_state == GameState.CREDITS:
                self.credits_playing.update()
                finished = self.credits_playing.draw(self.screen)
                if not finished or event.type == pygame.KEYDOWN:
                    current_state = GameState.MENU
                    pygame.mixer.music.stop()
                    self.back_to_menu()
            elif current_state == GameState.INTRO:
                if self.intro_scene is None:
                    self.intro()
                else:
                    self.intro_scene.handle_events(events)
                    self.intro_scene.update(dt)
                    self.intro_scene.draw(self.screen)

            pygame.display.update()
            pygame.display.flip()

        pygame.quit()
        exit()
