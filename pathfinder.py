import pygame, pytmx
import numpy as np
import conf

class PathFinder:
    def __init__(self,tiledmap):
        self.tm = tiledmap
        self.npc = None
        self.chasing = []
    def get_matrix_map(self):
        if self.tm:
            ncols = self.tm.tmxdata.width
            nfils = self.tm.tmxdata.height
            print("w:",ncols,"h:",nfils)
            mat = [[] for i in range(nfils)]
            objs = self._get_obj()
            free = 0
            occupied = 0
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
                    if collide:
                        occupied += 1
                    else:
                        free +=1
            print("Shape:",np.array(mat).shape)
            print("Free:",free,"Occupied:",occupied)
            return np.array(mat,dtype=int)
        else:
            raise ValueError("No TileMap object given")
    def _get_obj(self):
        if self.tm:
            for layer in self.tm.tmxdata.visible_layers:
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "buildings":
                        return [i for i in layer]
        else:
            raise ValueError("No TileMap object given")