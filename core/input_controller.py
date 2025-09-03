import pygame
from .state_manager import GameState


class InputController:
    def __init__(self, game):
        self.game = game
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if(self.game.state_manager.current_state == GameState.PLAYING):
                    if event.key == pygame.K_z:
                        #TODO : avancer vers le haut player.move_up()
                        print("avancer vers le haut")
                    elif event.key == pygame.K_s:
                        #TODO : avancer vers le bas player.move_down()
                        print("avancer vers le bas")
                    elif event.key == pygame.K_q:
                        #TODO : avancer vers la gauche player.move_left()
                        print("avancer vers la gauche")
                    elif event.key == pygame.K_d:
                        #TODO : avancer vers la droite player.move_right()
                        print("avancer vers la droite")