# coding=utf-8
import pygame
from pygame.locals import *
import math
from pgu import engine, gui
import conf
from tiledmap import TiledMap
from pytmx import TiledObjectGroup
import numpy as np
import champs
from bala import Bala
# from pathfinder import PathFinder
import zombie
from pausa import Pausa

class Joc(engine.Game):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla_zoom, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()

    def _init_state_machine(self):
        pygame.init()
        self.jugant = Jugant(self)
        self.menu = Menu(self)
        self.pausa = Pausa(self)
        
    def run(self):
        super().run(self.menu, self.screen)
    
    def change_state(self, transicio=None):
        print("Canviant a:",transicio)
        if self.state is self.menu:
            if transicio == "Jugar":
                new_state = self.jugant
                self.jugant.init()
            else:
                raise ValueError("Transició desconeguda:",transicio)
        elif self.state == self.jugant:
            if transicio=="Pausa":
                new_state = self.pausa
                self.pausa.init()
        elif self.state == self.pausa:
            if transicio=="Continuar":
                new_state = self.jugant
            elif transicio=="Menu":
                new_state = self.menu
                self.menu.init()
        else:
            raise ValueError("Estat desconegut:",self.state)
        return new_state

    def tick(self):
        self.crono.tick(conf.fps)

class Jugant(engine.State):
    def init(self):
        self.load_data()

    def load_data(self):
        self.map = TiledMap("Images/mapabo.tmx")
        self.transicio = ''
        # self.pf = PathFinder(self.map)
        self.gchamp = pygame.sprite.Group()
        self.champ = champs.Champ2(np.true_divide(self.map.camera.size,2),conf.mides_champ)
        self.gchamp.add(self.champ)
        self.pressed_keys = []
        self.llista_bales = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.z1 = zombie.Zombie(np.multiply(conf.tile_size,2))
        self.angle=0
        self.temps = pygame.time.get_ticks()
        self.quit = False

        #Musica:
        pygame.mixer.stop()
        pygame.mixer.set_num_channels(conf.num_canals)
        llista =[]
        for i in range(conf.num_canals):
            llista.append(pygame.mixer.Channel(i))
        self.llista_canals = llista
        self.llista_canals[0].play(pygame.mixer.Sound(conf.song_1))
        
    def paint(self, screen):
        self.update(screen)
    def event(self,evt):
        if evt.type == pygame.MOUSEBUTTONDOWN:
                bala = Bala(np.floor_divide(conf.mides_pantalla,2),self.angle)
                self.llista_bales.add(bala)
                v=self.llista_canals[0].get_volume()+0.5
                self.llista_canals[2].set_volume(v)
                self.llista_canals[2].play(pygame.mixer.Sound(conf.gun_sound))
        if evt.type == pygame.QUIT:
            self.quit = True
        if evt.type == pygame.KEYDOWN:
            k = evt.key
            if k in self.pressed_keys:
                del self.pressed_keys[self.pressed_keys.index(k)]
            self.pressed_keys.append(k)
            if k == pygame.K_x:
                self.pressed_keys = []
            if k==pygame.K_p:
                self.pressed_keys = []
                self.canvia_etapa("Pausa")
                self.llista_canals[3].play(pygame.mixer.Sound(conf.menu_song))
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

            #Canvi volum:
            if lk==pygame.K_UP:
                v = min(1,self.llista_canals[0].get_volume()+0.1)
                for i in self.llista_canals:
                    i.set_volume(v)
            elif lk==pygame.K_DOWN:
                v = max(0,self.llista_canals[0].get_volume()-0.1)
                for i in self.llista_canals:
                    i.set_volume(v)
            
        else:
            self.map.canviar_dir(4)
            self.champ.mov = False

    def loop(self):
        self.map.update()
        self.gchamp.update()
        self._avoidCollisions()
        self.llista_bales.update()
        pos_mouse=pygame.mouse.get_pos()
        
        vector= np.subtract(pos_mouse,np.floor_divide(conf.mides_pantalla_zoom,2))#vector jugador-mouse
        self.angle = -math.atan2(vector[1], vector[0]) * (180.0 / math.pi)#angle respecte l'horitzontal del vector

        if self.champ.mov == True and not self.llista_canals[1].get_busy():
            self.llista_canals[1].play(pygame.mixer.Sound(conf.so_passes))
        elif self.champ.mov==False:
            self.llista_canals[1].stop()

        if not self.llista_canals[0].get_busy():# and self.temps - pygame.time.get_ticks() > conf.temps_espera_musica + 70000:
            self.llista_canals[0].play(pygame.mixer.Sound(conf.song_1))
            self.temps = pygame.time.get_ticks()

        if self.transicio!='':
            pygame.mixer.stop()
            estat = self.game.change_state(self.transicio)
            self.transicio = ''
            return estat

        if self.quit:
            pygame.quit
        
    def update(self, screen):
        sur = pygame.Surface(conf.mides_pantalla)
        sur.fill(conf.color_fons)
        sur.blit(self.map.image, (0,0))
        self.llista_bales.draw(sur)   
        self.gchamp.draw(sur)
        sur = pygame.transform.scale(sur, conf.mides_pantalla_zoom)
        screen.blit(sur,sur.get_rect())
        
             
        pygame.display.flip()
    def canvia_etapa(self, transicio):
        self.transicio = transicio
    def _avoidCollisions(self):
        prect = self.champ.rect.copy() # Copiem el rectangle del champion/jugador per a poder modificar-lo lliurement 
        """
        el problema és que el rectangle que obtenim per a mostrar, és relatiu a la camera/pantalla visible i l'hem de moure perque les colisions tenen en compte
        la posicio dels edificis a escala "global" tenint en compte el rectangle en relacio al mapa sencer
        """
        prect.move_ip(0,prect.height//2) # Movem el rectangle verticalment cap avall 
        prect.height = prect.height//2  # Li donem al rectangle una alçada per a col·lisionar només la meitat inferior del cos
        prect = prect.move(self.map.camera.topleft) # Aquí és on li sumem la posició de la camera al rectangle per a passar a la referencia "gran"
        for obj in self.map._get_obj(): # Iterem cada objecte de la capa "buildings" del mapa
            r = pygame.Rect(np.add((obj.x,obj.y),self.map.initpos),(obj.width,obj.height))  # Creem un rectangle amb la informacio de l'edifici iterat
            if r.colliderect(prect):    # Comprovem si el rectangle de l'edifici col·lisiona amb el rectangle calculat global del nostre personatge
                print("Colliding, obj dim:",(r.left,r.top,r.width,r.height), "and prect:",prect)
                """
                A continuacio es fan les correccions en cas de col·lisió
                """

                if r.top < prect.bottom and self.champ.dir==self.champ.AVALL:
                    self.map.move((0,r.top-prect.bottom))
                elif r.bottom > prect.top and self.champ.dir==self.champ.AMUNT:
                    self.map.move((0,r.bottom-prect.top))
                elif r.right > prect.left and self.champ.dir==self.champ.ESQUERRA:
                    self.map.move((r.right-prect.left,0))
                elif r.left < prect.right and self.champ.dir==self.champ.DRETA:
                    self.map.move((r.left-prect.right,0))

            """
            També comprovem si les bales colisionen o surten de la pantalla i cridem el mètode .kill() que ens elimina el sprite de tots els grups
            """
            for b in self.llista_bales:
                br = b.rect.copy()  # Fem una còpia del rectangle de la bala
                br = br.move(self.map.camera.topleft) # Canviem el rectangle de la bala a referència global
                if r.colliderect(br) or not self.map.camera.contains(br):  
                    #Collision
                    b.kill()
class Menu(engine.State):
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
        if not self.musica.get_busy() and (self.temps - pygame.time.get_ticks()) > conf.temps_espera_musica:
            self.musica.play(pygame.mixer.Sound(conf.menu_song))
            self.temps = pygame.time.get_ticks()
        if self.transicio != '':
            pygame.mixer.stop()
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
