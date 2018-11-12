import pygame
from pygame.locals import *
import conf
from pgu import engine

class Menu(engine.State):
    def __init__(self, *args):
        super().__init__(*args)

    def init(self):
        pass

    def paint(self, screen):
        pass

    def event(self, evt):
        pass
    
    def loop(self):
        super().loop()
    def update(self, screen):
        pygame.display.flip()