import pygame
from pygame.locals import *
import sys
import math
PI = 3.14159265
fix = PI/2
STEP = 0.1
pygame.init()
screen = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()

def tree(rad,start,deg):
   
    #deg+=fix
    mod=0.5
    x,y = start
    end = (x+(rad*math.cos(PI*deg)),y+(rad*math.sin(PI*deg)))
    #print(end)
    pygame.draw.aaline(screen,(255,255,255),start,end)
    if rad>3:
        tree(rad*mod,end,deg+STEP)
        tree(rad*mod,end,deg-STEP)
        tree(rad*mod,end,deg)#/2)
        #tree(rad*mod,end,deg-STEP/2)
        





while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    STEP = 0.002*pygame.mouse.get_pos()[0]
    tree(400,(400,800),-0.5)
    pygame.display.flip()
    clock.tick(30)
