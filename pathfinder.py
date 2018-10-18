import pygame, pytmx
import numpy as np
import conf, json
import tiledmap
import a_algorithm as aal

class PathFinder:
    def __init__(self,tiledmap):
        self.tm = tiledmap
        self.nfils = self.tm.tmxdata.height
        self.ncols = self.tm.tmxdata.width
        self.npc = None
        self.chasing_list = []
        self.matrix_map = self.tm.matrix_map
    def add(self,parella):
        if parella not in self.chasing_list:
            self.chasing_list.append(parella)
    def update(self):
        for parella in self.chasing_list:
            chaser = parella[0]
            path = self.a_algorithm_findpath(parella).get_path()
            if chaser.waiting_order:
                chaser.set_order(path[1].pos)

    def a_algorithm_findpath(self,parella):
        c_ind = tuple(self._buscarIndex(parella[0].rect.center))
        t_ind = tuple(self._buscarIndex(parella[0].rect.center))
        return aal.find_best_path(c_ind,t_ind,self.matrix_map)

    def _buscarIndex(self,pos):
        return np.floor_divide(pos,conf.tile_size).astype(int)
    

class Block:
    """
    F = G + H
    F := score
    G := cost from chaser to square
    H := estimated cost from square to target
    """
    def __init__(self,pos,t_ind,parent=None):
        self.parent = parent
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.t_ind = t_ind
    def __getattr__(self,attr):
        if attr == "f":
            return self.g + self.h
        elif attr == "g":
            return self.calculate_g()
        elif attr == "h":
            return self.calculate_h()
    def __eq__(self,b):
        if isinstance(b,Block):
            return self.pos == b.pos
        else:
            return False
    def calculate_g(self):
        g = 0
        ap = self.parent
        while ap is not None:
            g += 1
            ap = ap.parent
        return g
    def get_path(self):
        path = [self]
        parent = self.parent
        while parent is not None:
            path.append(parent)
            parent = parent.parent
        return path
    def calculate_h(self):
        return sum(abs(np.subtract(self.t_ind,self.pos)))
    def __str__(self):
        return "<Block("+str(self.pos)+",f="+str(self.f)+",g="+str(self.g)+",h="+str(self.h)+")>"
    def __eval__(self):
        return str(self)
    def __repr__(self):
        return str(self)

def main():
    pygame.display.set_mode(conf.mides_pantalla)
    tm = tiledmap.TiledMap("Images/til.tmx")
    with open("tilmat.json","w") as f:
        f.write(json.dumps(tm.matrix_map.tolist()))
    print("Saved")
    pygame.quit()
if __name__ == "__main__":
    main()
