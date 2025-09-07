import pygame

from sys import exit
from os import environ

from services.resources import Resources

from menus.main_menu import MainMenu
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

        self.handlers = {
            GameState.INTRO: self.__handle_intro,
            GameState.PLAYING: self.__handle_playing,
            GameState.CREDITS: self.__handle_credits,
            GameState.LOSE: self.__handle_lose,
            GameState.WIN: self.__handle_win,
            GameState.MENU: self.__handle_menu,
        }

    # Factory qui permet de créer les différent état du jeu
    def intro(self): self.state_factory.create(GameState.INTRO)
    def play(self): self.state_factory.create(GameState.PLAYING)
    def credits(self): self.state_factory.create(GameState.CREDITS)
    def trigger_game_lose(self): self.state_factory.create(GameState.LOSE)
    def trigger_game_win(self): self.state_factory.create(GameState.WIN)
    def back_to_menu(self): self.state_factory.create(GameState.MENU)

    def retry_game(self):
        """Relance une nouvelle partie"""
        self.event_controller.reset()
        self.game_lose_menu = None
        self.game_win_menu = None
        self.play()


    def exit(self):
        self.running = False

    #########################################################
    # DIFFERENTES HANDLERS POUR CHAQUE ETAT
    #########################################################
    def __handle_intro(self, events, dt):
        if self.intro_scene is None:
            self.intro()
        else:
            self.intro_scene.handle_events(events)
            self.intro_scene.update(dt)
            self.intro_scene.draw(self.screen)
    
    def __handle_playing(self, events, dt):
        self.playing.update(dt)
        self.playing.draw(self.screen)
        if not pygame.mixer.music.get_busy():   
            pygame.mixer.music.play()

    def __handle_credits(self, events, dt):
        self.credits_playing.update()
        finished = self.credits_playing.draw(self.screen)
        if not finished or any(e.type == pygame.KEYDOWN for e in events):
            pygame.mixer.music.stop()
            self.back_to_menu()
    
    def __handle_lose(self, events, dt):
        if self.game_lose_menu:
            pygame.mixer.music.stop()
            self.game_lose_menu.draw(self.screen)
        else:
            # Initialiser l'écran Game Lose à la première image
            self.trigger_game_lose()

    def __handle_win(self, events, dt):
        if self.game_win_menu:
            pygame.mixer.music.stop()
            self.game_win_menu.draw(self.screen)
        else:
            # Initialiser l'écran Game Win à la première image
            self.trigger_game_win()

    def __handle_menu(self, events, dt):
        self.menu.update()
        self.menu.draw(self.screen)

    #########################################################


    def run(self):
        while self.running:
            events = pygame.event.get()
            dt = self.clock.tick(self.settings.FPS) / 1000

            self.event_controller.handle_events(events, dt)

            state = self.state_manager.get_current_state()

            # On récupère les actions a effectuer pour l'état courrant
            handler = self.handlers.get(state)
            if handler:
                handler(events, dt)

            pygame.display.update()
            pygame.display.flip()

        pygame.quit()
        exit()
