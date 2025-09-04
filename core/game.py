import pygame
import sys
from .settings import Settings
from .state_manager import StateManager, GameState
from .event_controller import EventController
from .playing import Playing
from components import Button, Text, Menu

class Game:
    def __init__(self):
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        self.playing = Playing(self, self.event_controller)
        self.running = True

        self.game_text = Text(self.settings.SCREEN_WIDTH // 2, 200, self.settings.GAME_TITLE, pygame.font.Font(None, 75))

        self.text_play = Text(0, 0, "VOLER !", pygame.font.Font(None, 40))
        self.button_play = Button(self.settings.SCREEN_WIDTH // 2, 400, 250, 80, self.text_play, "#909090", "#707070", None, self.play)

        self.text_exit = Text(0, 0, "FUIR", pygame.font.Font(None, 40))
        self.button_exit = Button(self.settings.SCREEN_WIDTH // 2, 500, 250, 80, self.text_exit, "#ff0000", "#cc0000", None, self.exit)

        self.menu = Menu(self.game_text, [self.button_play, self.button_exit], "#505050")

    def play(self):
        self.playing = Playing(self, self.event_controller)
        self.state_manager.change_state(GameState.PLAYING)

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
                pygame.display.update()
            elif current_state == GameState.PAUSED:
                # TODO: A réaliser
                pass
            elif current_state == GameState.MENU:
                self.menu.draw(self.screen)
                pass
            elif current_state == GameState.GAME_OVER:
                # TODO: A réaliser
                pass
            elif current_state == GameState.WIN:
                # TODO: A réaliser
                pass
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
