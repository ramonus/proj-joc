import pygame
from pygame.locals import *
import conf
from pgu import engine


class Jugant(engine.State):
    def init(self):
        pass

    def paint(self, screen):
        self.update(screen)
    
    def event(self,evt):
        pass

    def loop(self):
        pass
    
    def update(self, screen):
        pygame.display.flip()