import pygame
import pytmx
import conf

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
        self.big_image = self.make_map()
        self.bir = self.big_image.get_rect()
        self.camera.topright = self.bir.topright
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
            self.camera.bottom = self.height
        if r > self.width:
            self.vel = (0, y)
            self.camera.right = self.width
    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface