import pygame

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked = True
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    self.mouse_clicked = False
                    
        self.mouse_pos = pygame.mouse.get_pos()
        return True
        
    def is_key_pressed(self, key):
        return key in self.keys_pressed
        
    def is_mouse_clicked(self):
        return self.mouse_clicked
        
    def get_mouse_pos(self):
        return self.mouse_pos 