import pygame

class Dungeon(pygame.sprite.Sprite) :
    '''
    Représente la carte principale du jeu
    La carte est capable de passer de la carte du donjon à la carte du souterrain
    '''
    dungeonMap = pygame.image.load("./assets/map/dungeon.png")
    subMap = pygame.image.load("./assets/map/vents.png")
    trapdoorsMap = pygame.image.load("./assets/map/trapdoors.png")
    dungeonMask = pygame.mask.from_surface(dungeonMap)
    subMask = pygame.mask.from_surface(subMap)
    trapdoorsMask = pygame.mask.from_surface(trapdoorsMap)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Dungeon.dungeonMap
        self.mask = Dungeon.dungeonMask
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0

    def draw(self, screen : pygame.surface.Surface):
        '''
        Affiche la carte sur l'écran
        :param screen:
        '''
        screen.blit(self.image, self.rect)
        screen.blit(Dungeon.trapdoorsMap, self.rect)

    def switchMap(self):
        '''
        Echange les 2 cartes
        '''
        if self.image is Dungeon.dungeonMap :
            self.image = Dungeon.subMap
            self.mask = Dungeon.subMask
        else:
            self.image = Dungeon.dungeonMap
            self.mask = Dungeon.dungeonMask

    def move(self, x, y):
        '''
        Déplace le joueur su la carte
        :param x: déplacement X
        :param y: déplacement Y
        '''
        self.rect.move_ip(-x, -y)
