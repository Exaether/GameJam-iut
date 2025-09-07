import pygame

from sys import exit
from os import environ

from services.resources import Resources

from core.main_menu import MainMenu
from core.settings import Settings
from core.state_manager import StateManager, GameState 
from core.event_controller import EventController
from core.state_factory import StateFactory


class Game:
    def __init__(self):
        pygame.init()

        # Centre la fênetre de jeu sur le bureau
        environ['SDL_VIDEO_CENTERED'] = "true"

        self.settings = Settings()
        self.resources = Resources()
        self.screen = pygame.display.set_mode((self.settings.MENU_SCREEN_WIDTH, self.settings.MENU_SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        pygame.display.set_icon(self.resources.game_cover.image_surf)
        
        self.clock = pygame.time.Clock()
        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        
        self.menu = MainMenu(self.settings, self)
        self.playing = None
        self.intro_scene = None
        self.credits_playing = None
        self.game_lose_menu = None
        self.game_win_menu = None

        # Factory 
        self.state_factory = StateFactory(self)

        self.running = True

    # Factory qui permet de créer les différent état du jeu
    def intro(self): self.state_factory.create(GameState.INTRO)
    def play(self): self.state_factory.create(GameState.PLAYING)
    def credits(self): self.state_factory.create(GameState.CREDITS)
    def trigger_game_lose(self): self.state_factory.create(GameState.LOSE)
    def trigger_game_win(self): self.state_factory.create(GameState.WIN)
    def back_to_menu(self): self.state_factory.create(GameState.MENU)

    def retry_game(self):
        """Relance une nouvelle partie"""
        self.game_lose_menu = None
        self.game_win_menu = None
        self.play()


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
