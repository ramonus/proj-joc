import pygame, pytmx
import numpy as np
import conf
import tiledmap

class PathFinder:
    def __init__(self,tiledmap):
        self.tm = tiledmap
        self.nfils = self.tm.tmxdata.height
        self.ncols = self.tm.tmxdata.width
        self.npc = None
        self.chasing = []
        self.matrix_map = self.get_matrix_map()
    def get_matrix_map(self):
        if self.tm:
            ncols = self.ncols
            nfils = self.nfils
            print("w:",ncols,"h:",nfils)
            mat = [[] for i in range(nfils)]
            objs = self._get_obj()
            for fila in range(nfils):
                for columna in range(ncols):
                    r1 = pygame.Rect(np.multiply((columna,fila),conf.tile_size),conf.tile_size)
                    collide = False
                    for obj in objs:
                        r2 = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
                        c = r1.colliderect(r2)
                        if c:
                            collide = True
                            break
                    mat[fila].append(int(collide))
            return np.array(mat,dtype=int)
        else:
            raise ValueError("No TileMap object given")
    def add(self,parella):
        pass
    def a_algorithm(self,parella):
        chaser, target = parella[0],parella[1]
        c_ind = tuple(self._buscarIndex(chaser.rect.center))
        t_ind = tuple(self._buscarIndex(target.rect.center))
        c_block = Block(c_ind,t_ind)
        t_block = Block(t_ind,t_ind)
        open_list = [c_block]
        closed_list = []
        path = None
        iteration = 0
        while len(open_list)>0:
            if iteration%100==0:
                print(iteration)
            curr_b = sorted(open_list,key=lambda b: b.f)[0] # Block with smallest F
            closed_list.append(curr_b)
            del open_list[open_list.index(curr_b)]
            if t_block in closed_list:
                #path found
                path = closed_list[closed_list.index(t_block)]
                break
            adj_b = self._get_adj_blocks(curr_b,t_ind)
            print("blocs adjacents:",len(adj_b))
            for a_b in adj_b:
                if a_b in closed_list:
                    continue
                if a_b not in open_list:
                    print("Block not in open list")
                    open_list.append(a_b)
                    print("Open_list:",len(open_list))
                else:
                    print("Block in open list")
                    if a_b.g<open_list[open_list.index(a_b)].g:
                        open_list[open_list.index(a_b)].parent = a_b.parent
            iteration+=1
            print("Next Iteration:",iteration)
        print("Path:",path.g)
                    




    def _get_adj_blocks(self,b,t_ind):
        print("Get adj blocks executantse")
        adj = []
        x,y = b.x,b.y
        pp = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
        for a,b in pp:
            if a>=0 and a<self.ncols and b>=0 and b<self.nfils and self.matrix_map[b,a]==0:
                adj.append(Block((a,b),t_ind,b))
        return adj
    def _buscarIndex(self,pos):
        return np.floor_divide(pos,conf.tile_size).astype(int)
    def _get_obj(self):
        if self.tm:
            for layer in self.tm.tmxdata.visible_layers:
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "buildings":
                        return [i for i in layer]
        else:
            raise ValueError("No TileMap object given")

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
        return self.pos == b.pos
    def calculate_g(self):
        g = 0
        while self.parent:
            g += 1
        return g 
    def calculate_h(self):
        return sum(np.subtract(self.t_ind,self.pos))


def main():
    pygame.display.set_mode(conf.mides_pantalla)
    tm = tiledmap.TiledMap("Images/til.tmx")
    class rct:
        def __init__(self,center):
            self.center = center
    class Sp:
        def __init__(self,pos):
            self.rect = rct(pos)

    a = Sp((0,0))
    b = Sp((115,435))
    pf = PathFinder(tm)
    pf.a_algorithm((a,b))

if __name__ == "__main__":
    main()
