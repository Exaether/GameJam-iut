from pygame.sprite import spritecollide

from paths import *

from services.resources import Resources
from services.suspicion_service import SuspicionService

from entities.dungeon import Dungeon    
from entities.player import Player
from entities.enemy import Enemy
from entities.item_pickup_effect import ItemPickupEffect
from entities.exitDoor import ExitDoor

from core.hud import HUD

from services.map_loader import LevelLoader

class Playing:
    """Classe qui gère tout le jeu en cours, le core du jeu"""

    def __init__(self, game, event_controller):
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.ressource = Resources()
        self.map = Dungeon()
        self.exit_door = ExitDoor()
        self.player = Player(2538, 190)
        self.nb_items_max = 0

        event_controller.set_player(self.player)
        event_controller.set_map(self.map)
        event_controller.set_exit_door(self.exit_door)

        self.suspicion_service = SuspicionService(self.player)

        # Chargement des gardes et des items
        self.guards_list = LevelLoader.load_guards()
        self.item_list, self.nb_items_max = LevelLoader.load_items()

        self.suspicion_service.set_total_items_count(self.nb_items_max)

        # Affichage du score et gestionnaire d'effets
        self.hud = HUD(self.settings, self.player, self.suspicion_service)
        self.pickup_effects = ItemPickupEffect()



        # Reset les paramètres du garde (pour annuler les changements de stat dû à l'horloge si activé lors de la partie précédente)
        Enemy.GUARD_DEFAULT_SPEED = 1.8

    def update(self, dt):
        self.player.update(dt, self.map)
        self.hud.clock.update(self.player, self.guards_list)

        if self.map.layer == 1:
            # Vérification des collisions entre le player et les items
            collided_items = spritecollide(self.player, self.item_list, True)
            self.player.speed = self.player.SPEED_DEFAULT
            for item in collided_items:
                if item.pickable:
                    self.player.items_collected += 1
                    self.pickup_effects.add_pickup_animation(item.rect.centerx, item.rect.centery)
                    self.ressource.pickup_sound.play()
                    self.suspicion_service.verify_effect_suspicion_to_apply(self.guards_list)

            self.pickup_effects.update(dt)
        else:
            self.player.speed = self.player.SPEED_SUBTERRAN

        # Mettre à jour les gardes avec les collisions
        for guard in self.guards_list.sprites():
            # update seulement les gardes proches
            if abs(guard.x - self.player.rect.centerx) < (self.settings.GAME_SCREEN_WIDTH / 2 + 100) and\
                abs(guard.y - self.player.rect.centery) < (self.settings.GAME_SCREEN_HEIGHT / 2 + 100):
                if self.map.layer == 1:
                    if guard.is_player_detected(self.player, self.game.clock):
                        self.game.trigger_game_lose()
                        self.ressource.defeat_sound.play()
                guard.update(self.map)

        # Mettre a jour la boussole
        if len(self.item_list) > 0:
            self.hud.compass.update(self.player, self.item_list)

    def draw(self, screen):
        camera = (-self.player.rect.centerx + screen.get_rect().centerx,
                  -self.player.rect.centery + screen.get_rect().centery)
        screen.fill(self.settings.BACKGROUND_COLOR)
        self.map.draw(screen, camera)
        self.player.draw_spacebar(screen, camera, self.map, self.exit_door)

        if self.map.layer == 1:
            self.exit_door.draw(screen, camera)
            self.guards_list.draw(screen, camera, self.player)
            # self.item_list.draw(screen)
            for item in self.item_list.sprites():
                item.draw(screen, camera)
            self.pickup_effects.draw(screen, camera)

        self.player.draw(screen, camera)

        # Affichage du HUD (en dernier pour être au dessus de tout)
        self.hud.draw(screen, self.map.layer)