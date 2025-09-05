import pygame
import sys
import os

from .menu import Menu
from .settings import Settings
from .state_manager import StateManager, GameState
from .event_controller import EventController
from .playing import Playing
from components import GameLoseScreen, GameWinScreen

class Game:
    def __init__(self):
        pygame.init()

        # Centre la fênetre de jeu sur le bureaus
        os.environ['SDL_VIDEO_CENTERED'] = "true"

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        self.menu = Menu(self.settings, self)
        self.playing = Playing(self, self.event_controller)
        self.running = True

        self.game_lose_screen = None
        self.game_win_screen = None

    def play(self):
        self.screen = pygame.display.set_mode((self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT))
        self.playing = Playing(self, self.event_controller)
        self.state_manager.change_state(GameState.PLAYING)

    def retry_game(self):
        """Relance une nouvelle partie"""
        self.game_lose_screen = None
        self.game_win_screen = None
        self.screen = pygame.display.set_mode((self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT))
        self.play()
        
    def back_to_menu(self):
        """Retourne au menu principal"""
        self.game_lose_screen = None
        self.game_win_screen = None
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.state_manager.change_state(GameState.MENU)

    def trigger_game_lose(self):
        """Déclenche la défaite du jeu"""
        self.game_lose_screen = GameLoseScreen(
            self.settings.MENU_SCREEN_WIDTH,
            self.settings.MENU_SCREEN_HEIGHT,
            self.retry_game,
            self.back_to_menu
        )
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.state_manager.change_state(GameState.LOSE)

    def trigger_game_win(self):
        """Déclenche la victoire du jeu"""
        final_score = self.playing.player.items_collected
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        self.game_win_screen = GameWinScreen(
            self.settings.MENU_SCREEN_WIDTH,
            self.settings.MENU_SCREEN_HEIGHT,
            final_score,
            self.retry_game,
            self.back_to_menu
        )
        self.state_manager.change_state(GameState.WIN)

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
            elif current_state == GameState.PAUSED:
                # TODO: A réaliser
                pass
            elif current_state == GameState.MENU:
                self.menu.draw(self.screen)
            elif current_state == GameState.LOSE:
                if self.game_lose_screen:
                    self.game_lose_screen.draw(self.screen)
                else:
                    # Initialiser l'écran Game Lose à la première image
                    self.trigger_game_lose()
            elif current_state == GameState.WIN:
                if self.game_win_screen:
                    self.game_win_screen.draw(self.screen)
                else:
                    # Initialiser l'écran Game Win à la première image
                    self.trigger_game_win()

            pygame.display.update()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
