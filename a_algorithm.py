import conf, time
import json
import numpy as np
from PIL import Image

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

def get_adj_blocks(bl,t_ind,matrix_map):
        adj = []
        x,y = bl.x,bl.y
        ncols,nfils = matrix_map.shape
        pp = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
        for a,b in pp:
            if a>=0 and a<ncols and b>=0 and b<nfils and matrix_map[b,a]==0:
                adj.append(Block((a,b),t_ind,bl))
        return adj

def find_best_path(c_ind,t_ind,matrix_map):
    c_block = Block(c_ind,t_ind)
    t_block = Block(t_ind,t_ind)
    open_list = [c_block]
    closed_list = []
    path = None
    iteration = 0
    while len(open_list)>0:
        curr_b = sorted(open_list,key=lambda b: b.f)[0] # Block with smallest F
        closed_list.append(curr_b)
        del open_list[open_list.index(curr_b)]
        if t_block in closed_list:
            #path found
            path = closed_list[closed_list.index(t_block)]
            break
        adj_b = get_adj_blocks(curr_b,t_ind,matrix_map)
        for a_b in adj_b:
            if a_b in closed_list:
                continue
            if a_b not in open_list:
                open_list.append(a_b)
            else:
                if a_b.g<open_list[open_list.index(a_b)].g:
                    open_list[open_list.index(a_b)].parent = a_b.parent   
        iteration+=1
    return(path)
    
def main():
    with open("tilmat.json","r") as f:
        matrix_map = np.array(json.loads(f.read()))
    mm = [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
        
    ]
    mm = np.array(mm).astype(int)
    c_ind = (0,0)
    t_ind = (37,37)
    st = time.time()
    path = find_best_path(c_ind,t_ind,matrix_map)
    print("Path length:",path.g)
    et = time.time()-st
    print("Time elapsed: {:.2f}s".format(et))
    print(*path.get_path(),sep="\r\n")
    matrix_map = matrix_map.astype(float)
    for b in path.get_path():
        matrix_map[b.pos[1],b.pos[0]] = 0.5
    im = Image.fromarray(matrix_map*255)
    im = im.resize(np.multiply(im.size,10))
    im.show()
if __name__=="__main__":
    main()