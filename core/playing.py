import pygame
import os

from entities.compass import Compass
from entities.dungeon import Dungeon
from entities.player import Player
from entities.enemyGroup import EnemyGroup
from entities.enemy import Enemy
from entities.item import Item
from entities.item_pickup_effect import ItemPickupEffect
from entities.exitDoor import ExitDoor
from core.clock import Clock
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
        event_controller.set_exit_door(self.exit_door)

        self.guards_list = EnemyGroup()
        self.guard_generator()

        self.item_list = pygame.sprite.Group()
        self.items_generator()

        # Affichage du score et gestionnaire d'effets (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        self.score_font = pygame.font.Font(None, 36)
        self.pickup_effects = ItemPickupEffect()
        self.compass = Compass(self.settings.GAME_SCREEN_WIDTH/2, self.settings.GAME_SCREEN_HEIGHT/2)

        self.clock = Clock(self.settings.GAME_SCREEN_WIDTH)

    def guard_generator(self):
        with open(os.path.join("data", "guards.csv"), "r") as file:
            for line in file:
                parts = line.strip().split(",")
                
                if len(parts) < 7:
                    continue  # Ignore les lignes invalides

                x = int(parts[0])
                y = int(parts[1])
                min_x = int(parts[2])
                max_x = int(parts[3])
                min_y = int(parts[4])
                max_y = int(parts[5])
                type = parts[6]
                # Direction est optionnelle
                if len(parts) > 7:
                    direction = parts[7]
                    guard = Enemy(x, y, min_x, max_x, min_y, max_y, type, direction)
                else:
                    guard = Enemy(x, y, min_x, max_x, min_y, max_y, type)
                self.guards_list.add(guard)

    def items_generator(self):
        with open(os.path.join("data", "items.csv"), "r") as file:
            for line in file:
                parts = line.strip().split(",")
                
                if len(parts) != 2:
                    continue  # Ignore les lignes mal formatées

                try:
                    x = int(parts[0])
                    y = int(parts[1])
                    item = Item(x, y)
                    self.item_list.add(item)
                except ValueError:
                    continue  # Ignore les valeurs non numériques

    def update(self, dt):
        self.player.update(dt, self.map)
        self.clock.update()

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
                if guard.is_player_detected(self.player, self.game.clock):
                    self.game.trigger_game_lose()

            self.pickup_effects.update(dt)
        else:
            self.player.speed = self.player.SPEED_SUBTERRAN

        # Mettre à jour les gardes avec les collisions
        for guard in self.guards_list.sprites():
            # update seulement les gardes proches
            if abs(guard.rect.centerx - self.player.rect.centerx) < 350 or \
                abs(guard.rect.centery - self.player.rect.centery) < 350:
                guard.update(self.map)

        # Mettre a jour la boussole
        if len(self.item_list) > 0:
            self.compass.update(self.player, self.item_list)

    def draw(self, screen):
        camera = (-self.player.rect.centerx + screen.get_rect().centerx,
                  -self.player.rect.centery + screen.get_rect().centery)
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.map.draw(screen, camera)
        self.player.draw_spacebar(screen, camera, self.map, self.exit_door)

        if self.map.layer == 1:
            self.exit_door.draw(screen, camera)
            self.guards_list.draw(screen, camera, self.player)
            #self.item_list.draw(screen)
            for item in self.item_list.sprites():
                item.draw(screen, camera)
            self.pickup_effects.draw(screen, camera)
            # Boussole
            if len(self.item_list) > 0:
                self.compass.draw(screen)

        self.player.draw(screen, camera)

        # Affichage du score en haut à droite (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        score_text = self.score_font.render(f"Items: {self.player.items_collected}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (self.settings.GAME_SCREEN_WIDTH - 10, 10)
        screen.blit(score_text, score_rect)

        # Overlay de vision du joueur (gestion de l'obscurité) # TODO ; a voir si on décalle pas direct dans player car ça appartient au player
        self.player.draw_darkness_overlay(screen, camera, self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT)
        # TODO 
        #self.clock.draw(screen)

        if self.settings.DEBUG_MODE:
            self._draw_debug_info(screen)
            
    def _draw_debug_info(self, screen):
        """Affiche les informations de débogage à l'écran."""
        font = pygame.font.Font(None, 24)
        text = font.render(f"Position: {self.player.get_position()}", True, self.settings.WHITE)  
        screen.blit(text, (10, 10))
