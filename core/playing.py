import pygame

from entities.compass import Compass
from entities.dungeon import Dungeon
from entities.player import Player
from entities.enemyGroup import EnemyGroup
from entities.enemy import Enemy
from entities.item import Item
from entities.item_pickup_effect import ItemPickupEffect
from entities.exitDoor import ExitDoor
class Playing:
    """Classe qui gère tout le jeu en cours, le core du jeu"""
    
    def __init__(self, game, event_controller):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.map = Dungeon()
        self.exit_door = ExitDoor()
        self.player = Player(2538, 190)

        event_controller.set_player(self.player)
        event_controller.set_map(self.map)

        self.guards_list = EnemyGroup()
        guard = Enemy(250, 200, 100, 450, 100, 450, "square")
        guard2 = Enemy(2450, 326, 0, 0, 0, 0, "fixe", "left")
        self.guards_list.add(guard)
        self.guards_list.add(guard2)

        item = Item(self.settings.GAME_SCREEN_WIDTH // 2, self.settings.GAME_SCREEN_HEIGHT // 2)
        item2 = Item(self.settings.GAME_SCREEN_WIDTH // 4, self.settings.GAME_SCREEN_HEIGHT // 4)
        self.item_list = pygame.sprite.Group()
        self.item_list.add(item)
        self.item_list.add(item2)

        # Affichage du score et gestionnaire d'effets (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        self.score_font = pygame.font.Font(None, 36)
        self.pickup_effects = ItemPickupEffect()
        self.compass = Compass(self.settings.GAME_SCREEN_WIDTH/2, self.settings.GAME_SCREEN_HEIGHT/2)

    def update(self, dt):
        self.player.update(dt, self.map)
        if pygame.sprite.collide_mask(self.player, self.map):
            self.player.undo_move()

        if self.map.layer == 1:
            # Vérification des collisions entre le player et les items
            collided_items = pygame.sprite.spritecollide(self.player, self.item_list, True)
            self.player.speed = self.player.SPEED_DEFAULT
            for item in collided_items:
                if item.pickable:
                    self.player.items_collected += 1
                    self.pickup_effects.add_pickup_animation(item.rect.centerx, item.rect.centery)
            # Verifie si le joueur est dans la zone de vision d'au moins un garde, arrête le jeu si c'est le cas
            for guard in self.guards_list.sprites():
                if isinstance(guard, Enemy):
                    if guard.is_player_detected(self.player, self.game.clock):
                        self.game.trigger_game_lose()

            self.pickup_effects.update(dt)
        else:
            self.player.speed = self.player.SPEED_SUBTERRAN

        if self.exit_door.rect.colliderect(self.player.rect):
            self.game.trigger_game_win()

        # Mettre à jour les gardes avec les collisions
        for guard in self.guards_list.sprites():
            guard.update(self.map)

        # Mettre a jour la boussole
        if len(self.item_list) > 0:
            self.compass.update(self.player, self.item_list)

    def draw(self, screen):
        camera = (-self.player.rect.centerx + screen.get_rect().centerx,
                  -self.player.rect.centery + screen.get_rect().centery)
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.map.draw(screen, camera)
        self.player.draw(screen, camera)
        self.player.draw_spacebar(screen, camera, self.map)

        if self.map.layer == 1:
            self.guards_list.draw(screen, camera, self.player)
            #self.item_list.draw(screen)
            for item in self.item_list.sprites():
                item.draw(screen, camera)
            self.pickup_effects.draw(screen, camera)
            # Boussole
            if len(self.item_list) > 0:
                self.compass.draw(screen)

        # Affichage du score en haut à droite (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        score_text = self.score_font.render(f"Items: {self.player.items_collected}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (self.settings.GAME_SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)

        # Overlay de vision du joueur (gestion de l'obscurité) # TODO ; a voir si on décalle pas direct dans player car ça appartient au player
        self.player.draw_darkness_overlay(screen, camera, self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT)

        if self.settings.DEBUG_MODE:
            self._draw_debug_info(screen)
            
    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, self.settings.WHITE)  
        screen.blit(text, (10, 10))
