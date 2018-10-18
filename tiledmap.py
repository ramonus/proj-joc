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
        self.matrix_map = self.get_matrix_map()
        self.vel_module = 5
        self.vel = (0,0)
        self.mam = np.subtract(np.add((self.width,self.height),self.camera.size),conf.mides_champ).astype(int)
        self.initpos = np.subtract(np.floor_divide(conf.mides_pantalla,2),np.floor_divide(conf.mides_champ,2)).astype(int)
        self.big_image = self.make_map()
        self.bir = self.big_image.get_rect()
        self.camera.center = self.bir.width//2,self.initpos[1]+self.bir.height//4
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
        print(self.camera)
        if t < 0:
            self.vel = (x,0)
            self.camera.top = 0
            print("Set vel to:",self.vel,"and top to: 0")
        if l < 0:
            self.vel = (0,y)
            self.camera.left = 0
            print("Set vel to:",self.vel,"and left to: 0")
        if b > self.bir.height:
            self.vel = (x,0)
            self.camera.bottom = self.bir.height
            print("Set vel to:",self.vel,"and bottom to:",self.bir.height)
        if r > self.bir.width:
            self.vel = (0, y)
            self.camera.right = self.bir.right
            print("Set vel to:",self.vel,"and right to:",self.bir.right)
        print(self.camera)
    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height))
        temp_surface.fill(conf.color_fons)
        self.render(temp_surface)
        bs = pygame.Surface(self.mam)
        bs.fill(conf.color_fons)
        bs.blit(temp_surface,self.initpos)
        return bs
    def get_matrix_map(self):
        ncols = self.tmxdata.width
        nfils = self.tmxdata.height
        mat = [[] for i in range(nfils)]
        objs = self._get_obj()
        for fila in range(nfils):
            for columna in range(ncols):
                r1 = pygame.Rect(np.multiply((columna,fila),conf.tile_size),conf.tile_size)
                collide = False
                for obj in objs:
                    r2 = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
                    c = r1.colliderect(r2)
                    if c:
                        collide = True
                        break
                mat[fila].append(int(collide))
        return np.array(mat,dtype=int)
    def _get_obj(self):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "buildings":
                    return [i for i in layer]