import pygame

class Edifici(pygame.sprite.Sprite):
    def __init__(self, pos, typ):
        super().__init__()
        self.type = typ
        self.image = pygame.image.load("Images/edifici{}.png".format(typ+1))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos