import pygame
import sys
from .settings import Settings
from .state_manager import StateManager, GameState
from .event_controller import EventController
from .playing import Playing
from entities.enemyGroup import EnemyGroup
from entities.enemy import Enemy
from entities.item import Item
from entities.item_pickup_effect import ItemPickupEffect
from components import Button, Text, Menu

class Game:
    def __init__(self):
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        self.clock = pygame.time.Clock()
        
        self.state_manager = StateManager(initial_state=GameState.MENU)
        self.event_controller = EventController(self)
        self.playing = Playing(self, self.event_controller)
        self.running = True

        self.game_text = Text(self.settings.SCREEN_WIDTH // 2, 200, self.settings.GAME_TITLE, pygame.font.Font(None, 75))

        self.text_play = Text(0, 0, "VOLER !", pygame.font.Font(None, 40))
        self.button_play = Button(self.settings.SCREEN_WIDTH // 2, 400, 250, 80, self.text_play, "#909090", "#707070", None, self.play)

        self.text_exit = Text(0, 0, "FUIR", pygame.font.Font(None, 40))
        self.button_exit = Button(self.settings.SCREEN_WIDTH // 2, 500, 250, 80, self.text_exit, "#ff0000", "#cc0000", None, self.exit)

        self.menu = Menu(self.game_text, [self.button_play, self.button_exit], "#505050")

    def play(self):
        self.playing = Playing(self, self.event_controller)
        self.state_manager.change_state(GameState.PLAYING)

    def exit(self):
        self.running = False

    def run(self):
        guards_list = EnemyGroup()
        guard = Enemy(0, 0, 200, 0)
        guards_list.add(guard)

        item = Item(self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT // 2)
        item2 = Item(self.settings.SCREEN_WIDTH // 4, self.settings.SCREEN_HEIGHT // 4)
        item_list = pygame.sprite.Group()
        item_list.add(item)
        item_list.add(item2)

        # Affichage du score et gestionnaire d'effets (#TODO : a voir pour mettre dans une class HUD ou autre ??)
        score_font = pygame.font.Font(None, 36)
        pickup_effects = ItemPickupEffect()

        while self.running:
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.event_controller.handle_events(events)
            
            dt = self.clock.tick(self.settings.FPS) / 1000.0
            current_state = self.state_manager.get_current_state()
            
            if current_state == GameState.PLAYING:
                # TODO : A TOUT DEPLACER DANS LA CLASS GAMEPLAY qui sera renommé PLAYING
                self.playing.update(dt, events)

                # Vérification des collisions entre le player et les items #TODO : a voir pour une classe collision
                player_position = self.playing.player.get_center()
                items_to_remove = []

                for item in item_list:
                    if item.player_on_item(player_position):
                        self.playing.player.items_collected += 1
                        items_to_remove.append(item)
                        pickup_effects.add_pickup_animation(item.rect.centerx, item.rect.centery)

                # Suppression des items collectés
                for item in items_to_remove:
                    item_list.remove(item)

                # Mise à jour des effets de collecte
                pickup_effects.update(dt)

                self.playing.draw(self.screen)
                guards_list.update()
                guards_list.draw(self.screen)
                item_list.draw(self.screen)

                # Affichage des effets de collecte (#TODO : a voir pour mettre dans une class HUD ou autre ??)
                pickup_effects.draw(self.screen)

                # Affichage du score en haut à droite (#TODO : a voir pour mettre dans une class HUD ou autre ??)
                score_text = score_font.render(f"Items: {self.playing.player.items_collected}", True, (255, 255, 255))
                score_rect = score_text.get_rect()
                score_rect.topright = (self.settings.SCREEN_WIDTH - 10, 10)
                self.screen.blit(score_text, score_rect)

                # Verifie si le joueur est dans la zone de vision d'au moins un garde, arrête le jeu si c'est le cas
                for guard in guards_list.sprites():
                    if isinstance(guard, Enemy):
                        if guard.is_detection_area_colliding(self.playing.player.rect):
                            self.state_manager.change_state(GameState.MENU)
                pygame.display.update()
            elif current_state == GameState.PAUSED:
                # TODO: A réaliser
                pass
            elif current_state == GameState.MENU:
                self.menu.draw(self.screen)
                pass
            elif current_state == GameState.GAME_OVER:
                # TODO: A réaliser
                pass
            elif current_state == GameState.WIN:
                # TODO: A réaliser
                pass
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
