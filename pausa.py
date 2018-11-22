import pygame
import conf
from pgu import engine, gui
class Pausa(engine.State):
    def __init__(self, *args):
        super().__init__(*args)
        # gui
        self.app = gui.App()

        
    def init(self):
        self.transicio = ''
        self.temps = pygame.time.get_ticks()
        self.musica = pygame.mixer.Channel(1)
        pygame.mixer.stop()
        t = gui.Table()
        for text in ["Continuar","Menu"]:
            b = gui.Button(text,width=conf.menu_button_size[0],height=conf.menu_button_size[1])
            b.connect(gui.CLICK, self.canvia_etapa, text)
            t.td(b)
            t.tr()
        self.app.init(widget=t)

    def paint(self, screen):
        screen.fill(conf.color_fons_pausa)
        self.update(screen)

    def event(self, ev):
        r1 = super().event(ev)
        r2 = self.app.event(ev)
        return r1 or r2
    def loop(self):
        super().loop()
        if self.transicio != '':
            pygame.mixer.stop()
            estat = self.game.change_state(self.transicio)
            self.transicio == ''
            return estat
        if not self.musica.get_busy():# and (self.temps - pygame.time.get_ticks()) > conf.temps_espera_musica:
            self.musica.play(pygame.mixer.Sound(conf.menu_song))
            self.temps = pygame.time.get_ticks()
    def update(self, screen):
        super().update(screen)
        self.app.update(screen)
        pygame.display.flip()

    def canvia_etapa(self,text):
        self.transicio = text
