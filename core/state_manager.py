"""
Gestionnaire d'états pour les différents écrans du jeu
"""
from enum import Enum


class GameState(Enum):
    """Énumération des différents états du jeu"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    QUIT = "quit"


class StateManager:
    """Gère les transitions entre les différents états du jeu"""
    
    def __init__(self, initial_state=GameState.MENU):
        self.current_state = initial_state
        self.previous_state = None
        self.state_changed = False
        
    def change_state(self, new_state):
        """Change l'état actuel vers un nouvel état"""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_changed = True
            print(f"État changé: {self.previous_state.value} -> {self.current_state.value}")
    
    def is_state(self, state):
        """Vérifie si l'état actuel correspond à l'état donné"""
        return self.current_state == state
    
    def get_current_state(self):
        """Retourne l'état actuel"""
        return self.current_state
    
    def get_previous_state(self):
        """Retourne l'état précédent"""
        return self.previous_state
    
    def has_state_changed(self):
        """Vérifie si l'état a changé depuis la dernière vérification"""
        if self.state_changed:
            self.state_changed = False
            return True
        return False
    
    def should_quit(self):
        """Vérifie si le jeu doit se fermer"""
        return self.current_state == GameState.QUIT 