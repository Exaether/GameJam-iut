import pygame
import sys
from .settings import Param
from .input_handler import InputHandler


class Game:
    def __init__(self):
        pygame.init()
        
        self.params = Param()
        
        self.screen = pygame.display.set_mode((self.params.SCREEN_WIDTH, self.params.SCREEN_HEIGHT))
        pygame.display.set_caption(self.params.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        
        self.input_handler = InputHandler()
        
        self.running = True
        self.current_screen = "menu"
        
        self.font = pygame.font.Font(None, self.params.MENU_FONT_SIZE)
        
        self.menu_buttons = self._create_menu_buttons()
        
    def _create_menu_buttons(self):
        buttons = []
        
        play_text = self.font.render("Jouer", True, self.params.WHITE)
        play_rect = play_text.get_rect()
        play_rect.centerx = self.params.SCREEN_WIDTH // 2
        play_rect.centery = self.params.SCREEN_HEIGHT // 2 - self.params.MENU_BUTTON_HEIGHT
        buttons.append({"text": play_text, "rect": play_rect, "action": "play"})
        
        quit_text = self.font.render("Quitter", True, self.params.WHITE)
        quit_rect = quit_text.get_rect()
        quit_rect.centerx = self.params.SCREEN_WIDTH // 2
        quit_rect.centery = self.params.SCREEN_HEIGHT // 2 + self.params.MENU_BUTTON_HEIGHT
        buttons.append({"text": quit_text, "rect": quit_rect, "action": "quit"})
        
        return buttons
        
    def handle_menu_input(self):
        mouse_pos = self.input_handler.get_mouse_pos()
        
        if self.input_handler.is_mouse_clicked():
            for button in self.menu_buttons:
                if button["rect"].collidepoint(mouse_pos):
                    if button["action"] == "quit":
                        self.running = False
                    elif button["action"] == "play":
                        print("Bouton Jouer cliqué (pas encore implémenté)")
                        
    def update_menu(self):
        self.handle_menu_input()
        
    def draw_menu(self):
        self.screen.fill(self.params.BLACK)
        
        title_text = self.font.render("Mon Jeu", True, self.params.WHITE)
        title_rect = title_text.get_rect()
        title_rect.centerx = self.params.SCREEN_WIDTH // 2
        title_rect.centery = 150
        self.screen.blit(title_text, title_rect)
        
        mouse_pos = self.input_handler.get_mouse_pos()
        for i, button in enumerate(self.menu_buttons):
            color = self.params.BLUE if button["rect"].collidepoint(mouse_pos) else self.params.WHITE
            
            button_text = ["Jouer", "Quitter"][i]
            text = self.font.render(button_text, True, color)
            self.screen.blit(text, button["rect"])
            
    def update_game(self):
        # TODO: Implémenter la logique du jeu
        pass
        
    def draw_game(self):
        # TODO: Implémenter le rendu du jeu
        self.screen.fill(self.params.GRAY)
        
    def run(self):
        while self.running:
            events = pygame.event.get()
            
            if not self.input_handler.handle_events(events):
                self.running = False
                
            if self.current_screen == "menu":
                self.update_menu()
                self.draw_menu()
            elif self.current_screen == "game":
                self.update_game()
                self.draw_game()
                
            pygame.display.flip()
            self.clock.tick(self.params.FPS)
            
        pygame.quit()
        sys.exit() 