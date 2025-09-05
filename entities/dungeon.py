import pygame

class Dungeon(pygame.sprite.Sprite) :
    '''
    Représente la carte principale du jeu
    La carte est capable de passer de la carte du donjon à la carte du souterrain
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # images
        self.dungeonMap = pygame.image.load("./assets/map/dungeonSprite.png").convert_alpha()
        self.subMap = pygame.image.load("./assets/map/ventsSprite.png").convert_alpha()
        self.trapdoors = pygame.image.load("./assets/map/trapdoors.png").convert_alpha()
        # masks
        self.dungeonMask = pygame.mask.from_surface(pygame.image.load("./assets/map/dungeon.png").convert_alpha())
        self.subMask = pygame.mask.from_surface(pygame.image.load("./assets/map/vents.png").convert_alpha())
        self.trapdoorsMask = pygame.mask.from_surface(self.trapdoors)

        self.image = self.dungeonMap
        self.rect = self.image.get_rect()
        self.mask = self.dungeonMask
        self.rect.topleft = 0, 0
        self.prev_pos = self.rect.topleft
        # first layer (surface)
        self.layer = 1

    def draw(self, screen : pygame.surface.Surface, camera):
        '''
        Affiche la carte sur l'écran
        :param screen:
        '''
        screen.blit(self.image, self.rect.move(camera))
        screen.blit(self.trapdoors, self.rect.move(camera))

    def move(self, x, y):
        '''
        Déplace le joueur su la carte
        :param x: déplacement X
        :param y: déplacement Y
        '''
        self.prev_pos = self.rect.topleft
        self.rect.move_ip(-x, -y)

    def undo_move(self):
        self.rect.topleft = self.prev_pos

    def switch_map(self):
        '''
        Echange les 2 cartes
        :return:
        '''
        if self.layer == 1:
            self.layer = 0
            self.image = self.subMap
            self.mask = self.subMask
        else:
            self.layer = 1
            self.image = self.dungeonMap
            self.mask = self.dungeonMask

    def trapdoor_collide(self, player):
        offset_x = player.rect.x - self.rect.x
        offset_y = player.rect.y - self.rect.y
        return self.trapdoorsMask.overlap(player.mask, (offset_x, offset_y))