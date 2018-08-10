import pygame
import sys
import random
from pygame.locals import *


class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.walls = [1,1,1,1]#UP RIGTH DOWN LEFT
        self.visited = 0
        self.current = 0
    def drawshit(self):
        if self.current: color = (0,200,0)
        elif self.visited: color = (150,0,150)
        else: color = (100,100,100)
        x,y = self.x,self.y
        pygame.draw.rect(screen,color,((x*SIZE),(y*SIZE),SIZE,SIZE))
    def draw(self):
        x,y = self.x,self.y
        if self.walls[0]: pygame.draw.line(screen,WHITE,( x *SIZE,y*SIZE),((x+1)*SIZE,  y*SIZE)) #UP
        if self.walls[1]: pygame.draw.line(screen,WHITE,((x+1)*SIZE,(y)*SIZE),((x+1)*SIZE,(y+1)*SIZE)) #RIGHT
        if self.walls[2]: pygame.draw.line(screen,WHITE,((x)*SIZE,(y+1)*SIZE),((x+1)*SIZE,(y+1)*SIZE)) #DOWN
        if self.walls[3]: pygame.draw.line(screen,WHITE,((x)*SIZE,(y)*SIZE),((x)*SIZE,(y+1)*SIZE)) #LEFT



    def getneighbours(self):
        x,y = self.x,self.y
        arr = []
        if x-1>=0 and not field[x-1][y].visited:
            arr.append(field[x-1][y])
        if x+1<cells and not field[x+1][y].visited:
            arr.append(field[x+1][y])
        if y-1>=0 and not field[x][y-1].visited:
            arr.append(field[x][y-1])
        if y+1<cells and not field[x][y+1].visited:
            arr.append(field[x][y+1])
        return arr

    def remove(self,prev):
        if self.x == prev.x:
            if self.y > prev.y:
                k = 0
            else:
                k = 2
        else:
            if self.x > prev.x:
                k = 3
            else:
                k = 1
        self.walls[k] = 0
        prev.walls[k-2] = 0





SIZE = 20
WHITE = (255,255,255,75)
width,height = 800,800
cells = width//SIZE
field = [[Cell(x,y) for y in range(cells)] for x in range(cells)]
celarr = [x  for i in field for x in i]
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Corpse\'s labirynth ')
clock = pygame.time.Clock()




current = field[0][0]
current.visited = 1
current.current = 1
stack = [current]








ticker = 0
#main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            break
    

    if len(stack)>0:
        n = current.getneighbours()
        if len(n):
            current.current = 0
            prev = current
            current = random.choice(n)
            current.current = current.visited = 1
            stack.append(current)
            current.remove(prev)
        else:
            l = 0
            current.current = 0
            while l == 0 and len(stack)>0:
                current = stack.pop()
                l = len(current.getneighbours())
            current.current = current.visited = 1
    if ticker == 2:
        screen.fill((15,15,15))
        for cell in celarr:
            cell.drawshit()
        for cell in celarr:
            cell.draw()
        ticker = 0
        col = pygame.Color(255,255,255,0)
        ticker = 0
        pygame.display.flip()
    ticker+=1

    
    clock.tick(99999)
