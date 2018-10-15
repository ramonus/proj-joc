import pygame
import sprites
import conf

class Zombie(pygame.sprite.Sprite):
    # direccio
    AMUNT,AVALL,DRETA,ESQUERRA = range(4)
    def __init__(self,pos=(0,0)):
        super().__init__()
        im = pygame.image.load(conf.imatge_zombie)
        mat_imatges = sprites.crea_matriu_imatges(im,conf.mides_zombie_raw)
        # mat_imatges = self._escalar_matriu(mat_imatges,(40,40))
        self.carregar_imatges(mat_imatges)
        self.dir = self.DRETA
        self.mov = True
        self.count = 0
        self.image = self._carregarImatge()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def carregar_imatges(self,mi):
        self.stand_iarr = [
            mi[2][0:4],
            mi[6][0:4],
            mi[4][0:4],
            mi[0][0:4]
        ]
        self.walk_iarr = [
            mi[2][4:12],
            mi[6][4:12],
            mi[4][4:12],
            mi[0][4:12]
        ]
    def _escalar_matriu(self,matriu,nova_mida):
        nm = matriu.copy()
        for i in range(len(nm)):
            for j in range(len(nm[0])):
                nm[i][j] = pygame.transform.scale(nm[i][j],nova_mida)
        return nm
    def _carregarImatge(self):
        if self.mov:
            return self.walk_iarr[self.dir][self.count//5]
        else:
            return self.stand_iarr[self.dir][self.count]
    def update(self):
        self.count = self.count +1
        if (self.mov and self.count==8*5) or (not self.mov and self.count==4*5):
            self.count = 0
        self.image = self._carregarImatge()