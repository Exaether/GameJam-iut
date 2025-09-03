import pygame

from entities.dungeon import Dungeon
from entities.player import Player
from entities.enemyGroup import EnemyGroup
from entities.enemy import Enemy
from entities.item import Item
from entities.item_pickup_effect import ItemPickupEffect
from .state_manager import GameState

class Playing:
    """Classe qui gère tout le jeu en cours, le core du jeu"""
    
    def __init__(self, game, event_controller):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.map = Dungeon("./assets/map/dungeon.png")
        self.vents = Dungeon("./assets/map/vents.png")

        center_x = self.settings.SCREEN_WIDTH // 2
        center_y = self.settings.SCREEN_HEIGHT // 2
        self.player = Player(center_x, center_y)

        event_controller.set_player(self.player)

        self.guards_list = EnemyGroup()
        guard = Enemy(100, 200, 500, 200)
        self.guards_list.add(guard)

        item = Item(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2)
        item2 = Item(self.settings.SCREEN_WIDTH // 4, self.settings.SCREEN_HEIGHT // 4)
        self.item_list = pygame.sprite.Group()
        self.item_list.add(item)
        self.item_list.add(item2)

        # Affichage du score et gestionnaire d'effets (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        self.score_font = pygame.font.Font(None, 36)
        self.pickup_effects = ItemPickupEffect()

    def update(self, dt, events):
        self.player.update(dt)
        
        # Vérification des collisions entre le player et les items
        collided_items = pygame.sprite.spritecollide(self.player, self.item_list, True)
        
        for item in collided_items:
            if item.pickable: 
                self.player.items_collected += 1
                self.pickup_effects.add_pickup_animation(item.rect.centerx, item.rect.centery)

        self.pickup_effects.update(dt)
        self.guards_list.update()
        
        # Verifie si le joueur est dans la zone de vision d'au moins un garde, arrête le jeu si c'est le cas
        for guard in self.guards_list.sprites():
            if isinstance(guard, Enemy):
                if guard.is_player_detected(self.player.rect, self.game.clock):
                    self.game.state_manager.change_state(GameState.GAME_OVER)

        if pygame.sprite.collide_mask(self.player, self.map):
            self.player.undo_move()

    def draw(self, screen):
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.map.draw(screen)
        self.player.draw(screen)
        
        self.guards_list.draw(screen)
        self.item_list.draw(screen)
        self.pickup_effects.draw(screen)
        
        # Affichage du score en haut à droite (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        score_text = self.score_font.render(f"Items: {self.player.items_collected}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (self.settings.SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)
        
        if self.settings.DEBUG_MODE:
            self._draw_debug_info(screen)
            
    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, self.settings.WHITE)  
        screen.blit(text, (10, 10)) 