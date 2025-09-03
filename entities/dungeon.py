import pygame

class Dungeon(pygame.sprite.Sprite) :
    '''
    Représente la carte principale du jeu
    La carte est capable de passer de la carte du donjon à la carte du souterrain
    '''
    dungeonMap = pygame.image.load("../assets/map/dungeon.png")
    subMap = pygame.image.load("../assets/map/.png")
    dungeonMask = pygame.mask.Mask
    subMask = pygame.mask.Mask
    def __init__(self):
        self.image = Dungeon.dungeonMap
        self.mask = Dungeon.dungeonMask
        self.rect = self.image.get_rect()

    def draw(self, screen : pygame.surface.Surface):
        '''
        Affiche la carte sur l'écran
        :param screen:
        '''
        screen.blit(self.image, (0, 0))

    def switchMap(self):
        '''
        Echange les 2 cartes
        '''
        if self.image is Dungeon.dungeonMap :
            self.image = Dungeon.subMap
            self.mask = Dungeon.subMask