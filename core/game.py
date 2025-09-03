import pygame
import sys
from .settings import Settings
from .state_manager import StateManager, GameState
from .event_controller import EventController
from .gameplay import Gameplay

class Game:
    def __init__(self):
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        self.state_manager = StateManager(initial_state=GameState.PLAYING)
        self.event_controller = EventController(self)
        self.gameplay = Gameplay(self, self.event_controller)
        self.running = True
    
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
                self.gameplay.update(dt, events)
                self.gameplay.draw(self.screen)
            elif current_state == GameState.PAUSED:
                # TODO: A réaliser
                pass
            elif current_state == GameState.MENU:
                # TODO: A réaliser
                pass
            elif current_state == GameState.GAME_OVER:
                # TODO: A réaliser
                pass
            elif current_state == GameState.WIN:
                # TODO: A réaliser
                pass
            elif current_state == GameState.QUIT:
                self.running = False
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()