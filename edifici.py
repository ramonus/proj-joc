import pygame

class Edifici(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Images/edifici1.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos