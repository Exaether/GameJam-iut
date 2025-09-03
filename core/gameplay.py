import pygame
from entities.player import Player

class Gameplay:
    """Classe qui gère tout le gameplay, le core du jeu"""
    
    def __init__(self, game, event_controller):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings           
        
        center_x = self.settings.SCREEN_WIDTH // 2
        center_y = self.settings.SCREEN_HEIGHT // 2
        self.player = Player(center_x, center_y)

        event_controller.set_player(self.player)
    
    def update(self, dt, events):
        self.player.update(dt)
    
    def draw(self, screen):
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.player.draw(screen)
        
        if self.settings.DEBUG_MODE:
            self._draw_debug_info(screen)
            
    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, self.settings.WHITE)  
        screen.blit(text, (10, 10)) 