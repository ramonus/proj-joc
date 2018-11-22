import pygame
import sprites
import conf
import numpy as np

class BlackBone(pygame.sprite.Sprite):
    AMUNT,AVALL,DRETA,ESQUERRA = range(4)
    def __init__(self,pos=(0,0),escalar=None):
        super().__init__()
        im = pygame.image.load(conf.imatge_champ).convert_alpha()
        mat_imatges = sprites.crea_matriu_imatges(im, conf.mides_champ_raw)
        print(np.array(mat_imatges).shape)
        if escalar:
            mat_imatges = self._escalar_matriu(mat_imatges,escalar)
        self.carregar_imatges(mat_imatges)
        self.dir = self.AVALL
        self.mov = False
        self.count = 0
        self.image = self._carregarImatge()
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def carregar_imatges(self, mi):
        self.llista_im = [
            mi[0],
            mi[2],
            mi[1],
            mi[3]
        ]
    def _escalar_matriu(self,matriu,nova_mida):
        nm = matriu.copy()
        for i in range(len(nm)):
            for j in range(len(nm[0])):
                nm[i][j] = pygame.transform.scale(nm[i][j],nova_mida)
        return nm
    def _carregarImatge(self):
        return self.llista_im[self.dir][self.count//5]
    def update(self):
        if self.mov:
            self.count = self.count +1
            if self.count >= len(self.llista_im[self.dir])*5:
                self.count = 0
        else:
            self.count = 1*5
        self.image = self._carregarImatge()

class Champ2(pygame.sprite.Sprite):
    AMUNT,AVALL,DRETA,ESQUERRA = range(4)
    def __init__(self,pos=(0,0),escalar=None):
        super().__init__()
        im = pygame.image.load(conf.imatge_champ).convert_alpha()
        mat_imatges = sprites.crea_matriu_imatges(im, conf.mides_champ_raw)
        self.alpha = 3
        if escalar:
            mat_imatges = self._escalar_matriu(mat_imatges,escalar)
        self.carregar_imatges(mat_imatges)
        self.dir = self.AVALL
        self.mov = False
        self.count = 0
        self.image = self._carregarImatge()
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def carregar_imatges(self, mi):
        self.llista_im = [
            mi[3],
            mi[0],
            mi[2],
            mi[1]
        ]
    def _escalar_matriu(self,matriu,nova_mida):
        nm = matriu.copy()
        for i in range(len(nm)):
            for j in range(len(nm[0])):
                nm[i][j] = pygame.transform.scale(nm[i][j],nova_mida)
        return nm
    def _carregarImatge(self):
        return self.llista_im[self.dir][self.count//self.alpha]
    def update(self):
        if self.mov:
            self.count = self.count +1
            if self.count >= len(self.llista_im[self.dir])*self.alpha:
                self.count = 0
        else:
            self.count = 0
        self.image = self._carregarImatge()