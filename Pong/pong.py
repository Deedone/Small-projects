import pygame
from pygame.locals import *
import sys

pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

c = [100,100]
cs = [4,4]
p0 = [0,100]
p1 = [780,100]

keys = {K_UP:0,K_DOWN:0,K_w:0,K_s:0}

def moveball():
    global c
    c[0] += cs[0]
    c[1] += cs[1]
    if 585<c[1] or c[1]<15:
        cs[1] = - cs[1]
    if 770<c[0]:
        if abs(p1[1] - c[1]) < 100:
            cs[0] = - cs[0]
        else:
            c[0] = 400
    if c[0] < 30:
        if abs(p0[1] - c[1]) < 100:
            cs[0] = - cs[0]
        else:
            c[0] = 400
        
    
def movepads():
    if keys[K_UP]:
        p1[1]-=8
    if keys[K_DOWN]:
        p1[1]+= 8
    if keys[K_w]:
        p0[1]-=8
    if keys[K_s]:
        p0[1] += 8

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            break
        if event.type == KEYDOWN:
            keys[event.key] = 1
        if event.type == KEYUP:
            keys[event.key] = 0
    screen.fill((0,0,0))

    movepads()
    moveball()
    
    pygame.draw.circle(screen,(255,255,255),(c[0],c[1]),15)
    pygame.draw.rect(screen,(255,255,255),(p0[0],p0[1],20,100))
    pygame.draw.rect(screen,(255,255,255),(p1[0],p1[1],20,100))
    pygame.display.flip()

    clock.tick(60)
