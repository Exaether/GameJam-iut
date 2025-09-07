import pygame

from paths import get_asset_path

from services.resources import Resources
from services.vision_service import VisionService

from core.settings import Settings
class Player(pygame.sprite.Sprite):
    SPRITE_SIZE = 16
    SPEED_DEFAULT = 140
    SPEED_SUBTERRAN = 280
    ANIMATION_FRAMES = 4
    ANIMATION_SPEED = 0.2
    VISION_RANGE = 240
    VISION_ANGLE = 90
    SPACEBAR_WIDTH = 32
    SPACEBAR_HEIGHT = 16
    TRAPDOOR_ANIMATION_DURATION = 0.2

    DIRECTION_ROW = {
        "down": 0,
        "up": 16,
        "left": 32,
        "right": 48
    }

    def __init__(self, x=0, y=0):
        super().__init__()

        self.sprite_sheet = self._load_sprite_sheet()
        self.rect = pygame.Rect(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        self.speed = self.SPEED_DEFAULT
        self.items_collected = 0

        self.direction = "down"
        self.is_moving = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.is_traversing_trapdoor = False
        self.trapdoor_animation_timer = 0
        self.mask = pygame.mask.Mask((self.SPRITE_SIZE, self.SPRITE_SIZE), True)
        self.prev_pos = self.rect.center
        self.settings = Settings()

        self.__init_spacebar()

        self.vision_service = VisionService(self.VISION_RANGE, self.VISION_ANGLE)

    def __init_spacebar(self):
        spacebar_path = get_asset_path("other", "spacebar.png")
        self.spacebar = pygame.image.load(spacebar_path)
        self.spacebar_image = pygame.Surface([self.SPACEBAR_WIDTH, self.SPACEBAR_HEIGHT])
        self.spacebar_image.blit(self.spacebar, (0, 0), (0, 0, self.SPACEBAR_WIDTH, self.SPACEBAR_HEIGHT))
        self.spacebar_image.set_colorkey([0, 0, 0])

    def _load_sprite_sheet(self):
        sprite_path = get_asset_path("entities", "player_sprite.png")
        try:
            return pygame.image.load(sprite_path).convert_alpha()
        except pygame.error as e:
            print(f"Erreur lors du chargement du sprite sheet")
            return None

    def _get_sprite_rect(self, direction, frame):
        if self.sprite_sheet is None:
            return None

        x = self.DIRECTION_ROW.get(direction, self.DIRECTION_ROW["down"])
        y = frame * self.SPRITE_SIZE
        return pygame.Rect(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)

    def _get_current_sprite(self):
        sprite_surface = None
        if self.sprite_sheet is not None:
            sprite_surface = pygame.Surface((self.SPRITE_SIZE, self.SPRITE_SIZE), pygame.SRCALPHA)
            if self.is_traversing_trapdoor:
                sprite_rect = self._get_sprite_rect("down", 6) # dernier sprite de la premiere col du sprite sheet (position baissé)
            else:
                sprite_rect = self._get_sprite_rect(self.direction, self.animation_frame)
            sprite_surface.blit(self.sprite_sheet, (0, 0), sprite_rect)
        return sprite_surface

    def move(self, map, dx, dy, dt):
        if not self.is_traversing_trapdoor: # permet d'empecher les mouvements pendant la traversé de trap
            self.is_moving = True

            self.prev_pos = self.rect.center
            self.rect.x += int(dx * self.speed * dt)
            if map is not None and pygame.sprite.collide_mask(self, map):
                self.rect.x -= int(dx * self.speed * dt)

            self.rect.y += int(dy * self.speed * dt)
            if map is not None and pygame.sprite.collide_mask(self, map):
                self.rect.y -= int(dy * self.speed * dt)

            if dy < 0:
                self.direction = "up"
            elif dy > 0:
                self.direction = "down"

            if dx < 0:
                self.direction = "left"
            elif dx > 0:
                self.direction = "right"

    def undo_move(self):
        self.rect.center = self.prev_pos

    def idle(self):
        self.is_moving = False

    def animation_traverse_trapdoor(self):
        self.is_traversing_trapdoor = True
        self.trapdoor_animation_timer = 0
        Resources().pick_trapdoor_sound.play()

    def update(self, dt, dungeon_map=None):

        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.ANIMATION_SPEED:
                self.animation_frame = (self.animation_frame + 1) % self.ANIMATION_FRAMES
                self.animation_timer = 0
        elif self.is_traversing_trapdoor:
            self.trapdoor_animation_timer += dt
            if self.trapdoor_animation_timer >= self.TRAPDOOR_ANIMATION_DURATION:
                self.is_traversing_trapdoor = False
        else:
            self.animation_frame = 0
            self.animation_timer = 0

        self.vision_service.update_circular_vision(self.rect, dungeon_map)

    def draw_spacebar(self, surface, camera, map, exit_door):
        if map.trapdoor_collide(self) or exit_door.rect.colliderect(self.rect):
            x = self.rect.centerx - self.spacebar_image.get_width() / 2
            y = self.rect.top - self.spacebar_image.get_height()
            surface.blit(self.spacebar_image, (x + camera[0], y + camera[1]))

    def draw(self, screen, camera, show_vision=False):
        current_sprite = self._get_current_sprite()

        if show_vision:
            self.vision_service.draw_vision_cone(screen, camera)
        self.vision_service.draw_darkness_overlay(screen, camera, self.settings.GAME_SCREEN_WIDTH, self.settings.GAME_SCREEN_HEIGHT)    

        screen.blit(current_sprite, self.rect.move(camera))

    def get_position(self):
        # TODO : A voir si on garde, debug pour l'instant
        return self.rect.x, self.rect.y
