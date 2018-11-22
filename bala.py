import conf
import pygame
from pygame.locals import *
import math
class Bala(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self,pos,angle):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([1, 1])
        self.image.fill((255,255,0))
        self.angle=angle
        self.rect = self.image.get_rect()
        self.rect.center = pos

       
 
        
 
    def update(self):
        """ Move the bullet. """
        self.rect.centerx +=5*math.cos(self.angle*math.pi/180)
        self.rect.centery +=-5*math.sin(self.angle*math.pi/180)
       
        
