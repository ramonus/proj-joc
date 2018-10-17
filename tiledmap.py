import pygame
import pytmx
import conf
import numpy as np
class TiledMap:
    AMUNT,AVALL,DRETA,ESQUERRA,STOP = range(5)
    def __init__(self, fn):
        tm = pytmx.load_pygame(fn, pixelalpha=True, colorkey=None)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.camera = pygame.Rect((0,0),conf.mides_pantalla)
        self.vel_module = 2
        self.vel = (0,0)
        self.mam = np.subtract(np.add((self.width,self.height),self.camera.size),conf.mides_champ).astype(int)
        self.initpos = np.subtract(np.floor_divide(conf.mides_pantalla,2),np.floor_divide(conf.mides_champ,2)).astype(int)
        self.big_image = self.make_map()
        self.bir = self.big_image.get_rect()
        self.camera.center = self.initpos[0]+self.bir.width//2,self.initpos[1]+self.bir.width//4
        self.champ = pygame.Rect((0,0),conf.mides_champ)
        self.champ.center = self.camera.center
        self.image = self.big_image.subsurface(self.camera)

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
    def move(self,vec):
        self.camera = self.camera.move(vec)
        self.redo_image()
    def canviar_dir(self,d):
        if d==self.AMUNT:
            self.vel = (0,-self.vel_module)
        elif d==self.AVALL:
            self.vel = (0, self.vel_module)
        elif d==self.DRETA:
            self.vel = (self.vel_module,0)
        elif d==self.ESQUERRA:
            self.vel = (-self.vel_module,0)
        else:
            self.vel = (0,0)
    def update(self):
        self.move(self.vel)

    def redo_image(self):
        i=0
        while not self.bir.contains(self.camera) and i<10:
            print("Not fitting",self.camera)
            i += 1
            self._adjust_camera()
        self.image = self.big_image.subsurface(self.camera)

    def _adjust_camera(self):
        l,t = self.camera.topleft
        r,b = self.camera.bottomright
        x,y = self.vel
        if t < 0:
            self.vel = (x,0)
            self.camera.top = 0
        if l < 0:
            self.vel = (0,y)
            self.camera.left = 0
        if b > self.height:
            self.vel = (x,0)
            self.camera.bottom = self.bir.height
        if r > self.width:
            self.vel = (0, y)
            self.camera.right = self.bir.width
    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height))
        temp_surface.fill(conf.color_fons)
        self.render(temp_surface)
        bs = pygame.Surface(self.mam)
        bs.fill(conf.color_fons)
        bs.blit(temp_surface,self.initpos)
        return bs