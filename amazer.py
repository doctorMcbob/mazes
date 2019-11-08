import pygame
from pygame.locals import *

from random import choice, randint

pygame.init()

"""
amazer.py

playing around with different maze generators
making it up as i go

a maze will be a multi dimensional array
each cell in the array will be four bools representing the four exits of that cell
[N, E, S, W]
"""

SCREEN = pygame.display.set_mode((640, 480))
pygame.display.set_caption("wow thats a mazing")
PW = 32
W, H = 40, 40


# ** ** ** ** THE ALGORITHMS ** ** ** **
# holy cow this is fun
def first_draft():
    maze = blank_sheet()
    ent, ext = (4, 4), (W-4, H-4)
    heads = [ent]
    routes = {ent: [ent]}
    marked = []
    while ext not in heads and heads:
        x, y = heads.pop(0)
        route = routes[(x, y)]
        exits = maze[y][x]

        n = choice([2, 2, 3, 4])
        while sum(exits) < n:
            maze[y][x][randint(0, 3)] = 1
    
        for d, check in enumerate(exits):
            if check:
                x_, y_ = apply_direction(x, y, d)
                if x_ > 0 and y_ > 0 and x_ < W and y_ < H:
                    if (x_, y_) not in heads and (x_, y_) not in marked:
                        maze[y_][x_][(d + 2) % 4] = 1
                        heads.append((x_, y_))
                        routes[(x_, y_)] = route + [(x_, y_)]
                else:
                    maze[y][x][d] = 0
        marked.append((x, y))
    return drawn_maze(maze, ent, ext)

# # # # # # # # # # # # # # # # # # # # #

def issolvable(maze, ent, ext):
    checklist = [ent]
    highlighted = []
    while ext not in checklist:
        x, y = checklist.pop()
        highlighted.append((x, y))
        piece = maze[y][x]
        for d, check in enumerate(piece):
            if check:
                pos = apply_direction(x, y, d)
                if pos not in highlighted:
                    highlighted.append(pos)
    return highlighted

def apply_direction(x, y, d):
    return x + [0, 1, 0, -1][d], y + [-1, 0, 1, 0][d]
                                    
def blank_sheet():
    maze = []
    for Y in range(H):
        maze.append([])
        for X in range(W):
            maze[-1].append([0, 0, 0, 0])
    return maze

def drawn_maze(maze, ent, ext):
    surf = pygame.Surface((len(maze[0])*PW, len(maze)*PW))
    for Y, line in enumerate(maze):
        for X, cell in enumerate(line):
            if (X, Y) == ent:
                pygame.draw.rect(surf, (0, 0, 255), pygame.rect.Rect((X*PW + 2, Y*PW + 2), (PW - 4, PW - 4)))
            elif (X, Y) == ext:
                pygame.draw.rect(surf, (0, 255, 0), pygame.rect.Rect((X*PW + 2, Y*PW + 2), (PW - 4, PW - 4)))
            else:
                pygame.draw.rect(surf, (255, 255, 255), pygame.rect.Rect((X*PW + 2, Y*PW + 2), (PW - 4, PW - 4)))
            if cell[0]:
                pygame.draw.rect(surf, (255, 255, 255), pygame.rect.Rect((X*PW + 2, Y*PW), (PW - 4, 2)))
            if cell[1]:
                pygame.draw.rect(surf, (255, 255, 255), pygame.rect.Rect((X*PW + (PW - 2), Y*PW + 2), (2, PW - 4)))
            if cell[2]:
                pygame.draw.rect(surf, (255, 255, 255), pygame.rect.Rect((X*PW + 2, Y*PW + (PW - 2)), (PW - 4, 2)))
            if cell[3]:
                pygame.draw.rect(surf, (255, 255, 255), pygame.rect.Rect((X*PW, Y*PW + 2), (2, PW - 4)))
    return surf

############ MAIN LOOP #############
x, y = 0, 0
img = first_draft()
while True:
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(img, (x*PW, y*PW))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == QUIT: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                x += 1
            if e.key == K_LEFT:
                x -= 1
            if e.key == K_UP:
                y -= 1
            if e.key == K_DOWN:
                y += 1
