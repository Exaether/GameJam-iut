import pygame
from .state_manager import GameState

class EventController:
    def __init__(self, game):
        self.game = game
        self.player = None
    
    def set_player(self, player):
        self.player = player
    
    def handle_events(self, events):
        current_state = self.game.state_manager.get_current_state()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key, current_state)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event.pos, event.button, current_state)
            self.game.button_play.handle_event(event)
            self.game.button_exit.handle_event(event)
        
        if self.player and current_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            up_pressed = keys[pygame.K_z] or keys[pygame.K_UP]
            down_pressed = keys[pygame.K_s] or keys[pygame.K_DOWN]
            left_pressed = keys[pygame.K_q] or keys[pygame.K_LEFT]
            right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
            
            dx = dy = 0
            if up_pressed:
                dy -= 1
            if down_pressed:
                dy += 1
            if left_pressed:
                dx -= 1
            if right_pressed:
                dx += 1
            
            if dx != 0 or dy != 0:
                self.player.move(dx, dy)
            else:
                self.player.idle()
    
    def _handle_keydown(self, key, state):
        if state == GameState.PLAYING and self.player:
            # TODO : à définir
            pass
        
        elif state == GameState.MENU:
            # TODO : à définir
            pass
        
        elif state == GameState.PAUSED:
            # TODO : à définir
            pass
    
    def _handle_mousedown(self, pos, button, state):
        if state == GameState.MENU:
            pass