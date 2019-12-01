import pygame
from pygame.locals import *
from random import shuffle, choice, randint
pygame.init()
"""
similar to amazer.py, an exploration of procedural maze generation

the same but with the addition of up and down
this time the syntax will be Never Eat Soggy Waffles Unless Dared
[N, E, S, W, U, D] 
"""
PW = 16
W, H, L = 32, 32, 32

ENT = (randint(0, 31), randint(0, 31), randint(0, 31))
EXT = None

SCREEN = pygame.display.set_mode((PW * 20, PW * 20))
pygame.display.set_caption("take advantage of your spacial dimension")

def get(Q, X, Y, Z): return Q[Z][Y][X]

# algorithm

def first_draft():
    Q = blank()
    routes = {}
    # ...
    return Q, routes

def blank():
    floors = []
    for Z in range(L):
        floors.append([])
        for Y in range(H):
            floors[-1].append([])
            for X in range(W):
                floors[-1][-1].append([0, 0, 0, 0, 0, 0])
                


def draw(Q, floor, route=[]):
    surf = pygame.Surface((W*PW, H*PW))
    Z = floor
    for Y in range(H):
        for X in range(W):
            spot = get(Q, X, Y, Z)
            col = (255, 255, 255)
            if (X, Y, Z) == ENT: col = (0, 0, 255)
            elif (X, Y, Z) == EXT: col = (0, 255, 0)
            elif (X, Y, Z) in route: col = (255, 0, 0)
             if sum(cell): pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + PW/8, Y*PW + PW/8), (PW - (PW/8)*2, PW - (PW/8)*2)))
            if spot[0]: pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + PW/8, Y*PW), (PW - (PW/8)*2, PW/8)))
            if spot[1]: pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + (PW - (PW/8)), Y*PW + PW/8), (PW/8, PW - (PW/8)*2)))
            if spot[2]: pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + PW/8, Y*PW + (PW - (PW/8))), (PW - (PW/8)*2, PW/8)))
            if spot[3]: pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW, Y*PW + (PW/8)), (PW/8, PW - (PW/8)*2)))
            if spot[4]:
                pygame.draw.line(surf, (0, 0, 0), (X*PW, Y*PW), (X*PW+PW, Y*PW+PW/2))
                pygame.draw.line(surf, (0, 0, 0), (X*PW+PW, Y*PW+PW/2), (X*PW, Y*PW+PW))
            if spot[5]:
                pygame.draw.line(surf, (0, 0, 0), (X*PW+PW, Y*PW), (X*PW, Y*PW+PW/2))
                pygame.draw.line(surf, (0, 0, 0), (X*PW, Y*PW+PW/2), (X*PW+PW, Y*PW+PW))
    return surf

if __name__ == "__main__":
    Q, routes = first_draft()
    
