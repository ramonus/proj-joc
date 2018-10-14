import pygame
from pygame.locals import *

from pgu import engine
import conf
import edifici
from tiledmap import TiledMap
from pytmx.util_pygame import load_pygame

from scroll import Scroller

class Joc(engine.Game):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()

    def _init_state_machine(self):
        self.jugant = Jugant(self)

    def run(self):
        super().run(self.jugant, self.screen)

    def tick(self):
        self.crono.tick(conf.fps)

class Jugant(engine.State):
    def init(self):
        self.load_data()

    def load_data(self):
        """
        w,h = conf.mides_pantalla
        self.b = pygame.sprite.Group()
        e1 = edifici.Edifici((0,h//2),0)
        x1,y1 = e1.rect.bottomright
        e2 = edifici.Edifici((x1,y1),1)
        x2,y2 = e2.rect.bottomright
        e3  = edifici.Edifici((x2,y2),2)
        self.b.add(e1,e2,e3)
        self.tiled_map = load_pygame("Images/til.tmx")
        """
        self.map = TiledMap("Images/til.tmx")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()


    def paint(self, screen):
        self.update(screen)
    def loop(self):
        pass
    def update(self, screen):
        screen.fill(conf.color_fons)
        # self.b.draw(screen)
        screen.blit(self.map_img, (0,0))
        pygame.display.flip()
    
def main():
    game = Joc()
    game.run()

if __name__=="__main__":
    main()
