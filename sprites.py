import pygame

def crea_matriu_imatges(spritesheet, mides, marginx=0, marginy=0):
    w,h = spritesheet.get_width()
    nfils = (w+marginx)//(mides[0]+marginx)
    ncols = (h+marginy)//(mides[1]+marginy)
    matriu = [[] for i in range(nfils)]
    for fila in range(nfils):
        for columna in range(ncols):
            tros = pygame.Rect( ((mides[0]+marginx)*columna, (mides[1]+marginy)*fila), mides)
            matriu[fila].append(spritesheet.subsurface(tros))
    return matriu