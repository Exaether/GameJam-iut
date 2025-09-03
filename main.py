from core.game import Game
import pygame
from core.state_manager import StateManager
from core.state_manager import GameState
import sys

def main():
    game = StateManager()
    if game.state_manager.get_current_state() == GameState.GAME_OVER:
        pass
    if game.state_manager.get_current_state() == GameState.WIN:
        pass
    if game.state_manager.get_current_state() == GameState.PLAYING:
        pass
    if game.state_manager.get_current_state() == GameState.PAUSED:
        pass
    if game.state_manager.get_current_state() == GameState.MENU:
        pass
    if game.state_manager.get_current_state() == GameState.PAUSED:
        pass
    if game.state_manager.get_current_state() == GameState.MENU:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

if __name__ == "__main__":
    main() 