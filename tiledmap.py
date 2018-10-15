import pygame
import pytmx
import conf

class TiledMap:
    def __init__(self, fn):
        tm = pytmx.load_pygame(fn, pixelalpha=True, colorkey=None)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.camera = pygame.Rect((0,0,self.width//2,self.height//2))
        self.camera.center = self.width//2,self.height//2
        self.vel_module = 5
        self.vel = (0,0)
        self.big_image = self.make_map()
        self.bir = self.big_image.get_rect()
        self.image = self.big_image.subsurface(self.camera)
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
    def set_vel_x(self,vx):
        self.vel = (vx*self.vel_module, self.vel[1])
    def set_vel_y(self,vy):
        self.vel = (self.vel[0],vy*self.vel_module)
    def update(self):
        self.camera = self.camera.move(self.vel)
        i = 0
        while not self.bir.contains(self.camera) and i<10:
            print("Not fitting")
            i+=1
            self._adjust_camera()
        print(self.camera)
        self.image = self.big_image.subsurface(self.camera)
    def _adjust_camera(self):
        l,t = self.camera.topleft
        r,b = self.camera.bottomright
        if t < 0:
            self.set_vel_y(0)
            self.camera.top = 0
        if l < 0:
            self.set_vel_x(0)
            self.camera.left = 0
        if b > self.height:
            self.set_vel_y(0)
            self.camera.bottom = self.height
        if r > self.width:
            self.set_vel_x(0)
            self.camera.right = self.width
    def make_map(self):
        temp_surface = pygame.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface