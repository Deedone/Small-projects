import pygame
import math
import sys
import random
from pygame.locals import *

def getvariants():
    temp = points.copy()
    if random.randint(1,100) > 50:
        for i in range(random.randint(1,20)):
            a = random.randint(0,len(points)-2)
            b = a
            while b <= a:
                b = random.randint(a,len(points)-1)

            x = temp.pop(a)
            temp.insert(b,x)
        else:
            a = random.randint(0,len(points)-2)
            b = a
            while b <= a:
                b = random.randint(0,len(points)-1)
            sli = temp[a:b]
            sli.reverse()
            i = 0
            for x in sli:
                temp[a+i] = x
                i+=1
    return temp
def lentotal(t):
    s = 0
    for i in range(len(t)-1):
        s+=t[i].distto(t[i+1])
    return s
class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def distto(self, node):
        return math.sqrt((self.x-node.x)**2+(self.y-node.y)**2)

SIZE = 20
width,height = 800,800
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Corpse\'s mutator ')
clock = pygame.time.Clock()
children = 5000
points = [Point(random.randint(5,750),random.randint(5,750)) for _ in range(80)]

ticker = 0
#main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            break
    screen.fill((0,0,0))
    vari = [getvariants() for _ in range(children)]
    vari.append(points)
    vari.sort(key=lentotal)
    points = vari[0].copy()
    print(lentotal(points))
    #print("===\n",vari,"===")
    for p in points:
        pygame.draw.circle(screen,(255,255,255),(p.x,p.y),3)
    pygame.draw.lines(screen,(255,255,255),False,[(p.x,p.y) for p in points])
    pygame.display.flip()

    clock.tick(99)
