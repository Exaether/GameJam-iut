import pygame

from math import pi, radians, cos, sin
from typing import Tuple, Iterable, Optional
from enum import Enum


class VisionShape(Enum):
    CIRCLE = "circle"
    CONE = "cone"


class VisionService:
    """Gestion du champ de vision des entités"""

    DEFAULT_CIRCLE_RAYS = 72
    MIN_CONE_RAYS = 20
    MAX_CONE_RAYS = 40

    def __init__(self, vision_range: int = 100, vision_angle_degree: int = 60):
        self.vision_range = vision_range
        self.vision_angle_degree = vision_angle_degree

        # LOS (line of sight)
        self.vision_surface_los: Optional[pygame.Surface] = None
        self.vision_mask_los: Optional[pygame.mask.Mask] = None
        self.vision_rect: Optional[pygame.Rect] = None
        
        self.__direction_angles = {
            "right": 0.0,
            "down": pi / 2,
            "left": pi,
            "up": -pi / 2,
        }

        self.__temp_display_surface: Optional[pygame.Surface] = None
        self.__darkness_surface: Optional[pygame.Surface] = None
        self.__eraser_surface: Optional[pygame.Surface] = None

    def update_cone_vision(self, entity_rect: pygame.Rect, direction: str, dungeon_map=None):
        self.__update_vision_rect(entity_rect)
        self.__generate_surface_los(entity_rect, shape=VisionShape.CONE, direction=direction, dungeon_map=dungeon_map)

    def update_circular_vision(self, entity_rect: pygame.Rect, dungeon_map=None): 
        self.__update_vision_rect(entity_rect)
        self.__generate_surface_los(entity_rect, shape=VisionShape.CIRCLE, dungeon_map=dungeon_map)

    def is_target_in_vision(self, target):
        is_target_in_vision = False
        if self.vision_mask_los:
            offset = (target.rect.x - self.vision_rect.x, target.rect.y - self.vision_rect.y)
            is_target_in_vision = bool(self.vision_mask_los.overlap(target.mask, offset))
        return is_target_in_vision

    def draw_vision_cone(self, surface: pygame.Surface, camera: Tuple[int, int], color=(255, 255, 0, 64)):
        """Dessine la zone de vision (LOS)."""
        surface_los = self.vision_surface_los
        if surface_los and self.vision_rect:
            if (self.__temp_display_surface is None) or (self.__temp_display_surface.get_size() != surface_los.get_size()):
                self.__temp_display_surface = pygame.Surface(surface_los.get_size(), pygame.SRCALPHA)

            self.__temp_display_surface.fill((0, 0, 0, 0))
            self.__temp_display_surface.blit(surface_los, (0, 0))
            self.__temp_display_surface.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

            surface.blit(self.__temp_display_surface, self.vision_rect.move(camera).topleft)

    def draw_darkness_overlay(
        self,
        surface: pygame.Surface,
        camera: Tuple[int, int],
        screen_width: int,
        screen_height: int,
        darkness_color=(0, 0, 0, 180),
    ):
        """Avoir tout l'écran en noir sauf la zone de vision du plauer"""
        if (self.__darkness_surface is None) or (self.__darkness_surface.get_size() != (screen_width, screen_height)):
            self.__darkness_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

        self.__darkness_surface.fill(darkness_color)

        surface_los = self.vision_surface_los
        if surface_los and self.vision_rect:
            vsx, vsy = self.vision_rect.x + camera[0], self.vision_rect.y + camera[1]
            draw_x, draw_y = max(0, vsx), max(0, vsy)
            draw_w = min(surface_los.get_width(), screen_width - draw_x)
            draw_h = min(surface_los.get_height(), screen_height - draw_y)

            if draw_w > 0 and draw_h > 0:
                surface_los_x = max(0, -vsx)
                surface_los_y = max(0, -vsy)
                try:
                    clip = surface_los.subsurface((surface_los_x, surface_los_y, draw_w, draw_h))
                    if (self.__eraser_surface is None) or (self.__eraser_surface.get_size() != (draw_w, draw_h)):
                        self.__eraser_surface = pygame.Surface((draw_w, draw_h), pygame.SRCALPHA)

                    self.__eraser_surface.fill((0, 0, 0, 0))
                    self.__eraser_surface.blit(clip, (0, 0))
                    self.__eraser_surface.fill(darkness_color, special_flags=pygame.BLEND_RGBA_MULT)

                    self.__darkness_surface.blit(self.__eraser_surface, (draw_x, draw_y), special_flags=pygame.BLEND_RGBA_SUB)
                except ValueError:
                    pass

        surface.blit(self.__darkness_surface, (0, 0))

    def __generate_surface_los(self, entity_rect: pygame.Rect, shape: VisionShape, direction: Optional[str] = None, dungeon_map=None):
        surface_los = self.__create_transparent_surface_los(shape, entity_rect, direction, dungeon_map)
        self.vision_surface_los = surface_los
        self.vision_mask_los = pygame.mask.from_surface(surface_los)

    def __create_transparent_surface_los(self, shape: VisionShape, entity_rect: pygame.Rect, direction: Optional[str], dungeon_map):
        diameter = self.__diameter()
        surface = VisionService.__transparent_surface(diameter)
        local_center = (diameter // 2, diameter // 2)
        angles = self.__get_angles_los(shape, direction)
        polygon_points = self.__calculate_points_polygone_los(entity_rect, local_center, angles, dungeon_map)
        if len(polygon_points) > 2:
            pygame.draw.polygon(surface, (255, 255, 255, 255), polygon_points)
        return surface

    def __get_angles_los(self, shape: VisionShape, direction: Optional[str]):
        angles = []
        if shape == VisionShape.CIRCLE:
            angles = self.__generate_angles_circle()
        if shape == VisionShape.CONE:
            angle_base = self.__direction_to_angle(direction)
            demi_angle = radians(self.vision_angle_degree / 2)
            angles = self.__generate_angles_cone(angle_base, demi_angle)
        return angles

    def __calculate_points_polygone_los(self, entite_rect: pygame.Rect, local_center: tuple[int, int], angles, dungeon_map):
        world_center = (entite_rect.centerx, entite_rect.centery)
        return self.__los_polygon_points(world_center, local_center, angles, dungeon_map)

    def __generate_angles_cone(self, base_angle: float, half_angle_rad: float):
        # Détermine le nombre de rayons en fonction de l'angle de vision
        n = min(self.MAX_CONE_RAYS, max(self.MIN_CONE_RAYS, max(20, int(self.vision_angle_degree * 0.5))))
        step = (2 * half_angle_rad) / (n - 1) if n > 1 else 0
        angles = []
        for i in range(n):
            angles.append(base_angle - half_angle_rad + i * step)
        return angles

    def __generate_angles_circle(self):
        n = self.DEFAULT_CIRCLE_RAYS
        step = (2 * pi) / n
        angles = []
        for i in range(n + 1):
            angles.append(i * step)
        return angles

    def __los_polygon_points(
        self,
        world_center: Tuple[int, int],
        local_center: Tuple[int, int],
        angles: Iterable[float],
        dungeon_map,
    ):
        """Points du polygone LOS (raycasts sur chaque angle)."""
        cxw, cyw = world_center
        cxl, cyl = local_center
        pts = [(cxl, cyl)]
        for a in angles:
            d = self.__cast_ray((cxw, cyw), a, dungeon_map)
            pts.append((int(cxl + d * cos(a)), int(cyl + d * sin(a))))
        return pts

    def __cast_ray(self, start: Tuple[int, int], angle: float, dungeon_map):
        """Lance un rayon et retourne la distance d'intersection avec un obstacle ou la portée max (aucun obsatcle)"""
        distance_to_obstacle = float(self.vision_range)

        if dungeon_map:
            start_x, start_y = start
            direction_x, direction_y = cos(angle), sin(angle)

            step_size = 4
            current_distance = 0.0
            max_distance = float(self.vision_range)

            map_width, map_height = dungeon_map.mask.get_size()
            map_offset_x, map_offset_y = dungeon_map.rect.x, dungeon_map.rect.y

            obstacle_found = False

            while current_distance < max_distance:
                pixel_x = int(start_x + direction_x * current_distance)
                pixel_y = int(start_y + direction_y * current_distance)
                mask_x = pixel_x - map_offset_x
                mask_y = pixel_y - map_offset_y

                if 0 <= mask_x < map_width and 0 <= mask_y < map_height:
                    if dungeon_map.wallsMask.get_at((mask_x, mask_y)):
                        distance_to_obstacle = current_distance
                        obstacle_found = True

                if obstacle_found:
                    current_distance = max_distance
                else:
                    current_distance += step_size

                    # Plus augmenter la précision vers la fin du rayon
                    if current_distance > max_distance * 0.8:
                        step_size = 1

        return distance_to_obstacle

    @staticmethod
    def __transparent_surface(size: int):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        return surface

    def __diameter(self):
        return self.vision_range * 2

    def __direction_to_angle(self, direction: Optional[str]):
        direction_to_angle = 0.0
        if direction:
            direction_to_angle = self.__direction_angles.get(direction, 0.0)
        return direction_to_angle


    def __update_vision_rect(self, entity_rect: pygame.Rect):
        diameter = self.__diameter()
        self.vision_rect = pygame.Rect(
            entity_rect.centerx - self.vision_range,
            entity_rect.centery - self.vision_range,
            diameter,
            diameter,
        )
