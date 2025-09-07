import pygame

from core.state_manager import GameState

class EventController:
    def __init__(self, game):
        self.game = game
        self.player = None
        self.map = None
        self.exit_door = None
        self.is_player_in_trapdoor_animation = False
    
    def set_player(self, player):
        self.player = player

    def set_map(self, map):
        self.map = map

    def set_exit_door(self, exit_door):
        self.exit_door = exit_door
    
    def _get_buttons_for_state(self, game_state):
        """Retourne la liste des boutons pour un état de jeu donné"""
        buttons = []
        if game_state == GameState.MENU:
            buttons = [self.game.menu.button_play, self.game.menu.button_exit, self.game.menu.button_credits]
        elif game_state == GameState.LOSE and self.game.game_lose_menu:
            buttons = self.game.game_lose_menu.buttons
        elif game_state == GameState.WIN and self.game.game_win_menu:
            buttons = self.game.game_win_menu.buttons
        return buttons
    
    def _handle_buttons_hover(self, mouse_pos, game_state):
        """Gère le hover pour tous les boutons de l'état actuel"""
        buttons = self._get_buttons_for_state(game_state)
        for button in buttons:
            button.check_hover(mouse_pos)
    
    def _handle_buttons_click(self, mouse_pos, game_state):
        """Gère les clics pour tous les boutons de l'état actuel"""
        buttons = self._get_buttons_for_state(game_state)
        for button in buttons:
            button.check_click(mouse_pos)
    
    def handle_events(self, events, dt):
        """Gère les événements du jeu"""
        current_state = self.game.state_manager.get_current_state()
        
        self.__handle_trapdoor_animation()
        self.__handle_input_player_movement(dt, current_state)
        self.__handle_input_events(events, current_state)
    

    def __handle_trapdoor_animation(self):
        if self.is_player_in_trapdoor_animation and not self.player.is_traversing_trapdoor:
            self.map.switch_map()
            self.is_player_in_trapdoor_animation = False

    def __handle_input_events(self, events, current_state):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key, current_state)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mousedown(event.pos, current_state)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mousemotion(event.pos, current_state)
    
    def __handle_input_player_movement(self, dt, current_state):
        if self.player and current_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            
            up_pressed = keys[pygame.K_z] or keys[pygame.K_UP]
            down_pressed = keys[pygame.K_s] or keys[pygame.K_DOWN]
            left_pressed = keys[pygame.K_q] or keys[pygame.K_LEFT]
            right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]

            dx = right_pressed - left_pressed
            dy = down_pressed - up_pressed

            if dx != 0 or dy != 0:
                self.player.move(self.map, dx, dy, dt)
            else:
                self.player.idle()

    def _handle_keydown(self, key, state):
        if state == GameState.PLAYING:
            if self.map.trapdoor_collide(self.player) and key == pygame.K_SPACE:
                if not self.is_player_in_trapdoor_animation:
                    self.player.animation_traverse_trapdoor()
                    self.is_player_in_trapdoor_animation = True
            elif self.exit_door.rect.colliderect(self.player.rect) and key == pygame.K_SPACE:
                self.game.trigger_game_win()
    
    def _handle_mousedown(self, pos, state):
        """Gère les clics de souris pour tous les états"""
        if state in [GameState.MENU, GameState.LOSE, GameState.WIN]:
            self._handle_buttons_click(pos, state)

    def _handle_mousemotion(self, pos, state):
        """Gère le mouvement de souris pour tous les états"""
        if state in [GameState.MENU, GameState.LOSE, GameState.WIN]:
            self._handle_buttons_hover(pos, state)