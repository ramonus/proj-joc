import pygame
class Scroller(pygame.sprite.Sprite):
    def __init__(self, imatge, amplada):
        super().__init__()
        self.imatge_gran = amplia(imatge, amplada)
        self.finestra = pygame.Rect(0,0, amplada, self.imatge_gran.get_height())
        self.image = self.imatge_gran.subsurface(self.finestra)
        self.rect = self.image.get_rect()
    def update(self):
        self.finestra.left += 1
        if self.finestra.right > self.imatge_gran.get_width():
            self.finestra.left = 0
            self.image = self.imatge_gran.subsurface(self.finestra)

def amplia(imatge, amplada):
    ample, alt = imatge.get_size()
    nova_im = pygame.Surface((ample+amplada, alt))
    nova_im.blit(imatge, (0,0))
    nova_im.blit(imatge, (ample , 0))
    return nova_im
        