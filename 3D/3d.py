import pygame
from pygame.locals import *
import sys
import math

W = H = 600
D = 550#round((W/H) / 2)
ofs = 500 #round((W/H) / 2)
ox = round(W/2)
oy = round(H/2)

class Point():

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def get2d(self):
       
        k = D / (self.z + ofs)

        return ox + round(self.x*k), oy + round(self.y * k)

class Triangle():
    def __init__(self, p1,p2,p3):
        self.p = [p1,p2,p3]

    def draw(self,screen):
        #pygame.draw.circle(screen,(255,255,255),self.p[0].get2d(),3)
        #pygame.draw.circle(screen,(255,255,255),self.p[1].get2d(),3)
        #pygame.draw.circle(screen,(255,255,255),self.p[2].get2d(),3)
        pygame.draw.aaline(screen,(255,255,255),self.p[0].get2d(),self.p[1].get2d())
        pygame.draw.aaline(screen,(255,255,255),self.p[1].get2d(),self.p[2].get2d())
        pygame.draw.aaline(screen,(255,255,255),self.p[2].get2d(),self.p[0].get2d())

    def rotateZ(self, angle):
        xnbx = 1*math.cos(angle)
        xnby = 1*math.sin(angle)
        angle+=1.5708
        ynbx = 1*math.cos(angle)
        ynby = 1*math.sin(angle)
        

        for p in self.p:
            x = p.x
            y = p.y
            nx = x*xnbx+ y*xnby
            ny = x*ynbx + y*ynby
            p.x = nx
            p.y = ny
            
    def rotateX(self, angle):
        xnbx = 1*math.cos(angle)
        xnby = 1*math.sin(angle)
        angle+=1.5708
        ynbx = 1*math.cos(angle)
        ynby = 1*math.sin(angle)
        

        for p in self.p:
            x = p.x
            z = p.z
            nx = x*xnbx+ z*xnby
            nz = x*ynbx + z*ynby
            p.x = nx
            p.z = nz

##tr = [Triangle(Point(100,100,100),Point(100,100,-100), Point(-100,100,-100)),
##      Triangle(Point(100,100,100),Point(-100,100,100), Point(-100,100,-100)),
##
##      Triangle(Point(100,100,100),Point(100,100,-100), Point(0,-100,0)),
##      Triangle(Point(100,100,-100),Point(-100,100,-100), Point(0,-100,0)),
##      Triangle(Point(100,100,100),Point(-100,100,100), Point(0,-100,0)),]

tr = [Triangle(Point(100,100,100),Point(100,100,-100), Point(-100,100,-100)),
      Triangle(Point(100,100,100),Point(-100,100,100), Point(-100,100,-100)),
      Triangle(Point(100,-100,100),Point(100,-100,-100), Point(-100,-100,-100)),
      Triangle(Point(100,-100,100),Point(-100,-100,100), Point(-100,-100,-100)),
      Triangle(Point(100,100,100),Point(100,100,-100), Point(100,-100,-100)),
      Triangle(Point(100,100,100),Point(100,-100,-100), Point(100,-100,100)),
      Triangle(Point(100,100,100),Point(-100,100,100), Point(100,-100,100)),
      Triangle(Point(100,-100,100),Point(-100,100,100), Point(-100,-100,100)),

      Triangle(Point(-100,100,100),Point(-100,100,-100), Point(-100,-100,-100)),
      Triangle(Point(-100,100,100),Point(-100,-100,-100), Point(-100,-100,100)),
      Triangle(Point(100,100,-100),Point(-100,100,-100), Point(100,-100,-100)),
      Triangle(Point(100,-100,-100),Point(-100,100,-100), Point(-100,-100,-100)),
      ]

pygame.init()
screen = pygame.display.set_mode((W,H))

clock = pygame.time.Clock()
counter = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,0))
    if counter%2:
        for t in tr:
            t.draw(screen)
            t.rotateX(0.025)
    else:
        for t in tr:
            t.draw(screen)
            t.rotateX(0.025)
    counter+=1
   

    pygame.display.flip()
    clock.tick(60)






















    
