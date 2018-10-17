import pygame
from pygame.locals import *

from pgu import engine, gui
import conf
from tiledmap import TiledMap
from pytmx import TiledObjectGroup
import numpy as np
import champs
from PIL import Image
from pathfinder import PathFinder

class Joc(engine.Game):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla_zoom, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()

    def _init_state_machine(self):
        self.jugant = Jugant(self)
        self.menu = Menu(self)

    def run(self):
        super().run(self.menu, self.screen)
    
    def change_state(self, transicio=None):
        if self.state is self.menu:
            if transicio == "Jugar":
                new_state = self.jugant
                self.jugant.init()
            else:
                raise ValueError("Transició desconeguda:",transicio)
        else:
            raise ValueError("Estat desconegut:",self.state)
        return new_state

    def tick(self):
        self.crono.tick(conf.fps)

class Jugant(engine.State):
    def init(self):
        self.load_data()

    def load_data(self):
        self.map = TiledMap("Images/til.tmx")
        self.pf = PathFinder(self.map)
        ma = self.pf.get_matrix_map()
        im = Image.fromarray(ma*255)
        im = im.resize(np.multiply(im.size,10))
        im.show()

        self.gchamp = pygame.sprite.Group()
        self.champ = champs.Champ2(np.true_divide(self.map.camera.size,2),conf.mides_champ)
        self.gchamp.add(self.champ)
        self.pressed_keys = []


    def paint(self, screen):
        self.update(screen)
    def event(self,evt):
        if evt.type == pygame.KEYDOWN:
            k = evt.key
            if k in self.pressed_keys:
                del self.pressed_keys[self.pressed_keys.index(k)]
            self.pressed_keys.append(k)
            if k == pygame.K_x:
                self.pressed_keys = []
        elif evt.type == pygame.KEYUP:
            k = evt.key
            if k in self.pressed_keys:
                del self.pressed_keys[self.pressed_keys.index(k)]
        if len(self.pressed_keys)>0:
            lk = list(self.pressed_keys)[-1]
            if lk==pygame.K_w:
                self.map.canviar_dir(self.map.AMUNT)
                self.champ.dir = self.champ.AMUNT
                self.champ.mov = True
            elif lk==pygame.K_s:
                self.map.canviar_dir(self.map.AVALL)
                self.champ.dir = self.champ.AVALL
                self.champ.mov = True
            elif lk==pygame.K_a:
                self.map.canviar_dir(self.map.ESQUERRA)
                self.champ.dir = self.champ.ESQUERRA
                self.champ.mov = True
            elif lk==pygame.K_d:
                self.map.canviar_dir(self.map.DRETA)
                self.champ.dir = self.champ.DRETA
                self.champ.mov = True
        else:
            self.map.canviar_dir(4)
            self.champ.mov = False

    def loop(self):
        self.map.update()
        self.gchamp.update()
        self._avoidCollisions()
    def update(self, screen):
        sur = pygame.Surface(conf.mides_pantalla)
        sur.fill(conf.color_fons)
        sur.blit(self.map.image, (0,0))
        self.gchamp.draw(sur)
        sur = pygame.transform.scale(sur, conf.mides_pantalla_zoom)
        screen.blit(sur,sur.get_rect())
        pygame.display.flip()
    def _avoidCollisions(self):
        prect = self.champ.rect.copy()
        prect = prect.move(self.map.camera.topleft)
        for layer in self.map.tmxdata.visible_layers:
            if isinstance(layer, TiledObjectGroup):
                if layer.name == "buildings":
                    for obj in layer:
                        r = pygame.Rect(np.add((obj.x,obj.y),self.map.initpos),(obj.width,obj.height))
                        if r.colliderect(prect):
                            print("Colliding, obj dim:",(r.left,r.top,r.width,r.height), "and prect:",prect)
                            if r.top < prect.bottom and self.champ.dir==self.champ.AVALL:
                                self.map.move((0,r.top-prect.bottom))
                            elif r.bottom > prect.top and self.champ.dir==self.champ.AMUNT:
                                self.map.move((0,r.bottom-prect.top))
                            elif r.right > prect.left and self.champ.dir==self.champ.ESQUERRA:
                                self.map.move((r.right-prect.left,0))
                            elif r.left < prect.right and self.champ.dir==self.champ.DRETA:
                                self.map.move((r.left-prect.right,0))
class Menu(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        # gui
        self.app = gui.App()
    def init(self):
        self.transicio = ''
        t = gui.Table()
        for text in ["Jugar"]:
            b = gui.Button(text,width=conf.menu_button_size[0],height=conf.menu_button_size[1])
            b.connect(gui.CLICK, self.canvia_etapa, text)
            t.td(b)
            t.tr()
        self.app.init(widget=t)

    def paint(self, screen):
        screen.fill(conf.color_fons_menu)
        self.update(screen)

    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2
    def loop(self):
        super().loop()
        if self.transicio != '':
            return self.game.change_state(self.transicio)
    def update(self, screen):
        super().update(screen)
        self.app.update(screen)
        pygame.display.flip()

    def canvia_etapa(self,text):
        self.transicio = text
def main():
    game = Joc()
    game.run()

if __name__=="__main__":
    main()
