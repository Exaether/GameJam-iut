import pygame

class Dungeon(pygame.sprite.Sprite) :
    '''
    Représente la carte principale du jeu
    La carte est capable de passer de la carte du donjon à la carte du souterrain
    '''
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(map).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = 100, 0
        self.prev_pos = self.rect.topleft

    def draw(self, screen : pygame.surface.Surface, camera):
        '''
        Affiche la carte sur l'écran
        :param screen:
        '''
        screen.blit(self.image, self.rect.move(camera))

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
