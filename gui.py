import pygame
from pygame.locals import *
from pgu import engine, gui
import conf

class JocMenu(engine.Game):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.screen = pygame.display.set_mode(conf.mides_pantalla,SWSURFACE)
        self.crono = pygame.time.Clock()

        self.menu = Menu(self)
        self.play = Play(self)
    def run(self):
        super().run(self.menu, self.screen)

    def change_state(self, transition=None):
        if self.state is self.menu:
            if transition == 'JUGAR':
                self.play.init()
                new_state = self.play
            else:
                raise ValueError('Indicador de transició desconegut')
        else:
            raise ValueError('Estat de joc desconegut')
        return new_state

    def tick(self):
        self.crono.tick(conf.fps)

class Menu(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        self.app = gui.App()
    def init(self):
        self.transicio = ""
        t = gui.Table()
        for text in ['Jugar']:
            b = gui.Button(text)
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

    def canvia_etapa(self, text):
        self.transicio = text
class Play(engine.State):
    def init(self):
        self.image = pygame.Surface(conf.mides_pantalla)
        self.pos = 0,0
        self._pos = self.pos

    def paint(self,s):
        s.fill(conf.color_fons_play)

def main():
    game = JocMenu()
    game.run()

if __name__=="__main__":
    main()