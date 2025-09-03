import pygame
import sys
from .settings import Param
from .input_handler import InputHandler
from .state_manager import StateManager, GameState


class Game:
    def __init__(self):
        pygame.init()
        
        self.params = Param()
        
        self.screen = pygame.display.set_mode((self.params.SCREEN_WIDTH, self.params.SCREEN_HEIGHT))
        pygame.display.set_caption(self.params.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        
        self.input_handler = InputHandler()
        
        self.state_manager = StateManager()
        self.running = True
            
    def update_game(self):
        # TODO: Implémenter la logique du jeu
        pass
        
    def draw_game(self):
        # TODO: Implémenter le rendu du jeu
        pass
        
    def run(self):
        state_manager = StateManager()
    
        while True:
                if state_manager.get_current_state() == GameState.GAME_OVER:
                    pass
                if state_manager.get_current_state() == GameState.WIN:
                    pass
                if state_manager.get_current_state() == GameState.PLAYING:
                    Game().run()
                if state_manager.get_current_state() == GameState.PAUSED:
                    pass
                if state_manager.get_current_state() == GameState.MENU:
                    pass
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.update()