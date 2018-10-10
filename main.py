import pygame
from pygame.locals import *

from pgu import engine
import conf
import edifici

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
        w,h = conf.mides_pantalla
        self.b = pygame.sprite.Group()
        e = edifici.Edifici((w//2,h//2))
        self.b.add(e)
    def paint(self, screen):
        self.update(screen)
    def loop(self):
        pass
    def update(self, screen):
        screen.fill(conf.color_fons)
        self.b.draw(screen)
        pygame.display.flip()
    
def main():
    game = Joc()
    game.run()

if __name__=="__main__":
    main()
