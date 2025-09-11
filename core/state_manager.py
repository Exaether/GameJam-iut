from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PAUSED = "paused"
    INTRO = "intro"
    PLAYING = "playing"
    LOSE = "lose"
    WIN = "win"
    SCOREBOARD = "scoreboard"
    CREDITS = "credits"

class StateManager:
    
    def __init__(self, initial_state=GameState.MENU):
        self.current_state = initial_state
        self.previous_state = None
        self.state_changed = False
        
    def change_state(self, new_state):
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_changed = True
    
    def get_current_state(self):
        return self.current_state

