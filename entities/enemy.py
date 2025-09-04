import pygame
import math
from core.settings import Settings 
import os
import random

class Enemy(pygame.sprite.Sprite):

    SPRITE_SIZE = 16
    GUARD_SPEED = 1
    VISION_RANGE = 100
    VISION_ANGLE = 60

    def __init__(self, x_start, y_start, x_range_min, x_range_max, y_range_min, y_range_max, pattern_type="square"):
        super().__init__()
        self.sprite_path = os.path.join("assets", "entities", "enemy_sprite.png")
        self.sprite_sheet = pygame.image.load(self.sprite_path)
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.direction = "right"
        
        self.x = x_start
        self.y = y_start
        self.x_range_min = x_range_min
        self.x_range_max = x_range_max
        self.y_range_min = y_range_min
        self.y_range_max = y_range_max
        self.patrol_distance_x = random.randint(x_range_min, x_range_max)
        self.patrol_distance_y = random.randint(y_range_min, y_range_max)
        
        # Définir les étapes de patrouille # TODO : a générer automatiquement pour des patterns différents
        self.patrol_steps = [
            {'direction': 'right', 'dx': 1, 'dy': 0},
            {'direction': 'down', 'dx': 0, 'dy': 1},
            {'direction': 'left', 'dx': -1, 'dy': 0},
            {'direction': 'up', 'dx': 0, 'dy': -1}
        ]
        self.current_step_index = 0
        self.step_progress = 0
        
        self.alertness = 0
        self.exclamation_mark = pygame.image.load('assets/other/exclamation_mark.png')
        self.image_exclamation_mark = pygame.Surface([16, 16])
        self.image_exclamation_mark.blit(self.exclamation_mark, (0, 0), (0, 0, 16, 16))
        self.image_exclamation_mark.set_colorkey([0, 0, 0])
        
        # Pour les collisions avec les murs
        self.prev_x = self.x
        self.prev_y = self.y
        self.mask = pygame.mask.Mask((self.SPRITE_SIZE, self.SPRITE_SIZE), True)
        
        # Surface et mask pour la zone de détection
        self.vision_surface = None
        self.vision_mask = None
        self.vision_rect = None

    def get_image(self, x=0, y=0):
        self.image = pygame.Surface([self.SPRITE_SIZE, self.SPRITE_SIZE])
        self.image.blit(self.sprite_sheet, (0, 0), (x, y, self.SPRITE_SIZE, self.SPRITE_SIZE))
        self.image.set_colorkey([0, 0, 0])

    def set_direction(self, direction="right"):
        """Change la direction ou regarde l'entité"""
        if direction == "right":
            self.direction = "right"
            self.get_image(0, 0)
        elif direction == "left":
            self.direction = "left"
            self.get_image(16, 0)
        elif direction == "down":
            self.direction = "down"
            self.get_image(0, 0)
        elif direction == "up":
            self.direction = "up"
            self.get_image(16, 0)
        else:
            self.direction = direction

    def _create_vision_mask(self):
        """Crée le mask de collision pour la zone de vision"""

        # Créer une surface pour le cône de vision
        vision_size = self.VISION_RANGE * 2
        self.vision_surface = pygame.Surface((vision_size, vision_size), pygame.SRCALPHA)
        self.vision_surface.fill((0, 0, 0, 0))
        
        # Calculer les points du cône
        center_x = vision_size // 2
        center_y = vision_size // 2
        
        vision_angle = self._get_vision_angle()
        half_cone_angle = math.radians(self.VISION_ANGLE / 2)
        
        # Points du cône
        points = [(center_x, center_y)]
        for i in range(15):
            angle = vision_angle - half_cone_angle + (i * 2 * half_cone_angle / 14)
            x = center_x + self.VISION_RANGE * math.cos(angle)
            y = center_y + self.VISION_RANGE * math.sin(angle)
            points.append((x, y))
        
        # Dessiner le cône sur la surface
        pygame.draw.polygon(self.vision_surface, (255, 255, 255, 255), points)
        
        # Créer le mask et le rect
        self.vision_mask = pygame.mask.from_surface(self.vision_surface)
        self.vision_rect = pygame.Rect(
            self.rect.centerx - vision_size // 2,
            self.rect.centery - vision_size // 2,
            vision_size, vision_size
        )

    def _get_vision_angle(self):
        """Retourne l'angle de vision en radians selon la direction"""
        direction_angles = {
            "right": 0,
            "down": math.pi / 2,
            "left": math.pi,
            "up": -math.pi / 2
        }
        return direction_angles.get(self.direction, 0)

    def is_player_in_vision(self, player):
        """Vérifie si le joueur est dans la zone de vision par collision"""
        if self.vision_mask and self.vision_rect:
            
            # Calculer l'offset du joueur par rapport à la zone de vision
            offset_x = player.rect.x - self.vision_rect.x
            offset_y = player.rect.y - self.vision_rect.y
            
            # Tester la collision entre le mask du joueur et celui de la zone de vision
            return self.vision_mask.overlap(player.mask, (offset_x, offset_y))

    def draw_vision_cone(self, surface, camera):
        """Dessine le cône de vision de l'ennemi"""
        if self.vision_surface and self.vision_rect:
            # Créer une surface temporaire avec transparence pour l'affichage
            display_surface = pygame.Surface(self.vision_surface.get_size(), pygame.SRCALPHA)
            display_surface.blit(self.vision_surface, (0, 0))
            # Changer la couleur pour l'affichage (jaune transparent)
            display_surface.fill((255, 255, 0, 64), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(display_surface, self.vision_rect.move(camera).topleft)

    def draw_detection_area(self, surface):
        """Dessine la zone de détection du garde"""
        self.draw_vision_cone(surface)

    """
    Dessine un point d'exclamation au dessus du garde si le joueur est dans sa zone de détection
    """
    def draw_exclamation_mark(self, surface, camera):
        """Dessine un point d'exclamation au dessus du garde si le joueur est dans sa zone de détection"""
        if self.alertness > 0:
            x = self.rect.centerx - self.image_exclamation_mark.get_width()/2
            y = self.rect.top - self.image_exclamation_mark.get_height()
            surface.blit(self.image_exclamation_mark, (x + camera[0], y + camera[1]))

    def draw(self, surface, camera):
        """Dessine l'ennemi avec sa zone de détection et son point d'exclamation"""
        # Dessiner la zone de détection
        self.draw_vision_cone(surface, camera)
        
        # Dessiner le sprite de l'ennemi
        surface.blit(self.image, self.rect.move(camera))
        
        # Dessiner le point d'exclamation si en alerte
        self.draw_exclamation_mark(surface, camera)

    def is_player_detected(self, player, clock):
        """Vérifie si le joueur est détecté dans le cône de vision"""
        settings = Settings()
        if self.is_player_in_vision(player):
            self.alertness += clock.tick(settings.FPS)
        else:
            self.alertness = 0
        return self.alertness >= 200 # temps en millisecondes avant que le joueur se fasse attraper

    def undo_move(self):
        """Annule le dernier mouvement (pour les collisions)"""
        self.x = self.prev_x
        self.y = self.prev_y
        self.rect.topleft = (self.x, self.y)

    def update(self, dungeon_map=None):
        """Met à jour la position de l'ennemi avec mouvement en carré et gestion des collisions"""
        # Sauvegarder la position actuelle
        self.prev_x = self.x
        self.prev_y = self.y
        
        # Déterminer l'étape actuelle
        current_step = self.patrol_steps[self.current_step_index]
        dx = current_step['dx']
        dy = current_step['dy']
        
        # Appliquer le mouvement
        self.x += dx * self.GUARD_SPEED
        self.y += dy * self.GUARD_SPEED
        
        # Mettre à jour la direction
        self.set_direction(current_step['direction'])
        
        # Mettre à jour le progrès de l'étape
        self.step_progress += self.GUARD_SPEED
        
        # Vérifier si l'étape est terminée
        if self.step_progress >= self.patrol_distance_x or self.step_progress >= self.patrol_distance_y:
            self.current_step_index = (self.current_step_index + 1) % len(self.patrol_steps)
            self.step_progress = 0
            self.patrol_distance_x = random.randint(self.x_range_min, self.x_range_max)
            self.patrol_distance_y = random.randint(self.y_range_min, self.y_range_max)

        # Mettre à jour la position du rect
        self.rect.topleft = (self.x, self.y)
        
        # Vérifier les collisions avec les murs
        if dungeon_map and pygame.sprite.collide_mask(self, dungeon_map):
            self.undo_move()
            self.step_progress = self.patrol_distance_x
        
        # Mettre à jour la zone de vision
        self._create_vision_mask()