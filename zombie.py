import pygame
import sprites
import conf

class Zombie(pygame.sprite.Sprite):
    # direccio
    AMUNT,AVALL,DRETA,ESQUERRA = range(4)
    def __init__(self,pos=(0,0)):
        super().__init__()
        im = pygame.image.load(conf.imatge_zombie).convert_alpha()
        mat_imatges = sprites.crea_matriu_imatges(im,conf.mides_zombie_raw)
        if conf.mides_zombie!=conf.mides_zombie_raw:
            mat_imatges = self._escalar_matriu(mat_imatges,conf.mides_zombie)
        self.carregar_imatges(mat_imatges)
        self.dir = self.AVALL
        self.mov = False
        self.vel_module = 3
        self.waiting_order = True
        self.count = 0
        self.image = self._carregarImatge()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.alpha = 5
        self.dest = None
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
            return self.walk_iarr[self.dir][self.count//self.alpha]
        else:
            return self.stand_iarr[self.dir][self.count//self.alpha]
    def set_order(self,i_dest):
        self.waiting_order = False
        self.dest = i_dest
    def _buscarIndex(self,pos):
        return np.floor_divide(pos,conf.tile_size).astype(int)
    def update(self):
        self.count = self.count +1
        # Moure's a la destinacio
        rd = self._get_rect_from_ind(self.dest)
        vec = np.subtract(rd.center,self.rect.center)
        self.vel = np.floor_divide(vec,np.linalg.norm(vec))
        self.rect = self.rect.move(self.vel)
        if (self.mov and self.count>=8*self.alpha) or (not self.mov and self.count>=4*self.alpha):
            self.count = 0
        self.image = self._carregarImatge()

    def _get_rect_from_ind(self,ind):
        return pygame.Rect(np.multiply(ind,conf.tile_size),conf.tile_size)
