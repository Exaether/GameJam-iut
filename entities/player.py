import pygame
import os

class Player(pygame.sprite.Sprite):
    SPRITE_SIZE = 16
    SPEED_DEFAULT = 2
    SPEED_SUBTERRAN = 4
    ANIMATION_FRAMES = 4
    ANIMATION_SPEED = 0.2
    
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
        self.mask = pygame.mask.Mask((self.SPRITE_SIZE, self.SPRITE_SIZE), True)
        self.prev_pos = self.rect.center
        
    def _load_sprite_sheet(self):
        sprite_path = os.path.join("assets", "entities", "player_sprite.png")
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
            sprite_surface.blit(self.sprite_sheet, (0, 0), self._get_sprite_rect(self.direction, self.animation_frame))
        return sprite_surface
    
    def move(self, dx, dy):
        self.is_moving = True
        
        speed = self.speed
        # TODO: Y a une méthode normalize dans la librairie math sinon
        # Normaliser la vitesse pour les mouvements diagonaux
        if dx != 0 and dy != 0:
            speed *= 0.707  # Approximativement 1/sqrt(2)

        self.prev_pos = self.rect.center
        self.rect.x += int(dx * speed)
        self.rect.y += int(dy * speed)

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

    def update(self, dt):
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.ANIMATION_SPEED:
                self.animation_frame = (self.animation_frame + 1) % self.ANIMATION_FRAMES
                self.animation_timer = 0
        else:
            self.animation_frame = 0
    
    def draw(self, screen, camera):
        current_sprite = self._get_current_sprite()

        screen.blit(current_sprite, self.rect.move(camera))

    def get_position(self):
        return self.rect.x, self.rect.y
