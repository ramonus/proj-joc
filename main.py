import pygame
from pygame.locals import *
from pgu import engine
from Jugant import Jugant   # Carreguem la classe Jugant del fitxer Jugant.py
from Menu import Menu       # Carreguem la classe Menu del fitxer Menu.py
import conf # Carreguem l'arxiu conf.py per a la configuració local

class Joc(engine.Game): # Creem la classe Joc
    def __init__(self): # Definim el mètode __init__
        super().__init__() # Cridem el mètode __init__ de la classe heredada
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE) # Creem la pantalla i li passem les mides
        self.crono = pygame.time.Clock() # Creem el rellotge
        self._init_state_machine()  # Cridem la funció _init_state_machine
    
    def _init_state_machine(self):
        self.jugant = Jugant(self) # Creem i guardem la classe Jugant
        self.menu = Menu(self)  # Creem i guardem la classe Menu

    def run(self):
        super().run(self.menu, self.screen) # Cridem el mètode run de la classe heredada

    def change_state(self, transicio=None): # Definim mètode per canviar els estats
        if self.state is self.menu: # Si l'estat actual és el menu
            if transicio == conf.t_jugar:   # Si la transició és conf.t_jugar
                nou_estat = self.jugant     # Declarem el nou estat com al joc
                self.jugant.init()          # Iniciem de nou el joc
            else:
                raise ValueError("Transició desconeguda:",transicio)    # Si la transició és desconeguda fem saltar un error
        elif self.state == self.jugant:     # Si l'estat actual és el joc
            if transicio==conf.t_menu:      # Si la transició és conf.t_menu
                nou_estat = self.menu       # Declarem el nou estat com al menu
            else:
                raise ValueError("Transició desconeguda:",transicio)    # Si la transició és desconeguda fem saltar un error
        else:
            raise ValueError("Estat desconegut:",self.state)    # Si l'estat és desconegut fem saltar un error
        return nou_estat    # Retornem el nou estat

    def tick(self):
        self.crono.tick(conf.fps)   # Fem que el joc tingui una velocitat definida a conf.py

def main():
    game = Joc()
    game.run()

if __name__=="__main__":
    main()