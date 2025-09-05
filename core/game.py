import pygame
import sys

from .menu import Menu
from .settings import Settings
from .state_manager import StateManager, GameState
from .event_controller import EventController
from .playing import Playing
from components import GameLoseScreen, GameWinScreen


class Game:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        self.menu = Menu(self.settings, self)
        self.playing = Playing(self, self.event_controller)
        pygame.mixer.music.load('./assets/music/10-8bit10loop.ogg')
        self.running = True

        self.game_lose_screen = None
        self.game_win_screen = None

    def play(self):
        self.playing = Playing(self, self.event_controller)
        pygame.mixer.music.play()
        self.state_manager.change_state(GameState.PLAYING)

    def retry_game(self):
        """Relance une nouvelle partie"""
        self.game_lose_screen = None
        self.game_win_screen = None
        self.play()

    def back_to_menu(self):
        """Retourne au menu principal"""
        self.game_lose_screen = None
        self.game_win_screen = None
        self.state_manager.change_state(GameState.MENU)

    def trigger_game_lose(self):
        """Déclenche la défaite du jeu"""
        self.game_lose_screen = GameLoseScreen(
            self.settings.SCREEN_WIDTH,
            self.settings.SCREEN_HEIGHT,
            self.retry_game,
            self.back_to_menu
        )
        pygame.mixer.music.stop()
        self.state_manager.change_state(GameState.LOSE)

    def trigger_game_win(self):
        """Déclenche la victoire du jeu"""
        final_score = self.playing.player.items_collected
        self.game_win_screen = GameWinScreen(
            self.settings.SCREEN_WIDTH,
            self.settings.SCREEN_HEIGHT,
            final_score,
            self.retry_game,
            self.back_to_menu
        )
        pygame.mixer.music.stop()
        self.state_manager.change_state(GameState.WIN)

    def exit(self):
        self.running = False

    def run(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.event_controller.handle_events(events)

            dt = self.clock.tick(self.settings.FPS) / 1000.0
            current_state = self.state_manager.get_current_state()

            if current_state == GameState.PLAYING:
                self.playing.update(dt, events)
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
