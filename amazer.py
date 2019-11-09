import pygame
from pygame.locals import *

from random import choice, randint
import sys

pygame.init()

"""
amazer.py

playing around with different maze generators
making it up as i go

a maze will be a multi dimensional array
each cell in the array will be four bools representing the four exits of that cell
[N, E, S, W]
"""
PW = 16
W, H = 40, 40

SCREEN = pygame.display.set_mode((32 * 20, 32 * 20))
pygame.display.set_caption("wow thats a mazing")


# ** ** ** ** THE ALGORITHMS ** ** ** **
# holy cow this is fun
def breadth_first():
    maze = blank_sheet()
    ent = randint(0, W-1), randint(0, H-1)
    ext = randint(0, W-1), randint(0, H-1)
    while abs(ext[0] - ent[0]) + abs(ext[1] - ent[1]) < (W + H) / 2:
        ext = randint(0, W-1), randint(0, H-1)
        ent = randint(0, W-1), randint(0, H-1)
    heads = [ent]
    routes = {ent: [ent]}
    marked = []
    while heads or ext not in marked:
        if not heads:
            heads.append(choice(marked))
        x, y = heads.pop(0)
        route = routes[(x, y)]
        exits = maze[y][x]
        debug(maze, (x, y), ext, route=routes[(x, y)])
        n = choice([2, 2, 3, 4])
        while sum(exits) < n:
            maze[y][x][randint(0, 3)] = 1

        for d, check in enumerate(exits):
            if check:
                x_, y_ = apply_direction(x, y, d)
                if x_ >= 0 and y_ >= 0 and x_ < W and y_ < H:
                    if (x_, y_) not in heads and (x_, y_) not in marked:
                        maze[y_][x_][(d + 2) % 4] = 1
                        heads.append((x_, y_))
                        routes[(x_, y_)] = route + [(x_, y_)]
                    elif maze[y_][x_][(d + 2) % 4] == 0:
                        maze[y][x][d] = 0
                else: maze[y][x][d] = 0
        marked.append((x, y))
    return maze, ent, ext, routes[ext]

def depth_first():
    maze = blank_sheet()
    ent = randint(0, W-1), randint(0, H-1)
    ext = randint(0, W-1), randint(0, H-1)
    while abs(ext[0] - ent[0]) + abs(ext[1] - ent[1]) < (W + H) / 2:
        ext = randint(0, W-1), randint(0, H-1)
        ent = randint(0, W-1), randint(0, H-1)
    heads = [ent]
    routes = {ent: [ent]}
    marked = []
    while heads or (not ext in marked):
        if not heads:
            heads.append(choice(marked))
        x, y = heads.pop()
        debug(maze, (x, y), ext, route=routes[(x, y)])
        route = routes[(x, y)]
        exits = maze[y][x]

        n = choice([2, 2, 3, 4])
        while sum(exits) < n:
            maze[y][x][randint(0, 3)] = 1

        for d, check in enumerate(exits):
            if check:
                x_, y_ = apply_direction(x, y, d)
                if x_ >= 0 and y_ >= 0 and x_ < W and y_ < H:
                    if (x_, y_) not in heads and (x_, y_) not in marked:
                        maze[y_][x_][(d + 2) % 4] = 1
                        heads.append((x_, y_))
                        routes[(x_, y_)] = route + [(x_, y_)]
                    elif maze[y_][x_][(d + 2) % 4] == 0:
                        maze[y][x][d] = 0
                else: maze[y][x][d] = 0
        marked.append((x, y))
    return maze, ent, ext, routes[ext]

# # # # # # # # # # # # # # # # # # # # #

def issolvable(maze, ent, ext, no_pass=None, checkless=False):
    checklist = [(ent[0], ent[1], 0)]
    highlighted = {(ent[0], ent[1]): 0} # slot : distance
    while ext not in highlighted:
        if not checklist: return False
        x, y, dist = checklist.pop()
        piece = maze[y][x]
        for d, check in enumerate(piece):
            if check or checkless:
                x_, y_ = apply_direction(x, y, d)
                if no_pass:
                    for sx, sy in no_pass: # sx for start x...
                        ex, ey = no_pass[(sx, sy)] # ex for end x...
                        if sx == ex:# horizontal line
                            if max(sy, ey) > y > min(sy, ey) and min([x, x_]) == sx-1 and max([x, x_]) == sx:
                                continue
                        elif sy == ey: # verticle line
                            if max(sx, ex) > x > min(sx, ex) and min([y, y_]) == sy-1 and min([x, x_]) == sy:
                                continue
                if W > x_ > 0 and H > y_ > 0:
                    continue
                if (x_, y_) not in highlighted:
                    highlighted[(x_, y_)] = dist + 1
                    checklist.append((x_, y_, dist + 1))
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

def debug(maze, pos1, pos2, lines={}, pause=False, route=False):
    for spos in lines:
        pygame.draw.line(SCREEN, (255, 0, 0), (pos1[0]*PW, pos1[1]*PW), (pos2[0]*PW, pos2[1]*PW))
    SCREEN.blit(drawn_maze(maze, pos1, pos2, route=route, lit=True), (0, 0))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == QUIT: quit()
    while pause:
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE: pause = False    
    

def drawn_maze(maze, ent, ext, route=None, lit=False):
    surf = pygame.Surface((len(maze[0])*PW, len(maze)*PW))
    for Y, line in enumerate(maze):
        for X, cell in enumerate(line):
            col = (255, 255, 255)
            if (X, Y) == ent:
                col = (0, 0, 255)
            elif (X, Y) == ext:
                col = (0, 255, 0)
            elif route and (X, Y) in route:
                col = (255, 0, 0)
            if sum(cell) or lit:
                pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + 2, Y*PW + 2), (PW - 4, PW - 4)))
            if cell[0]:
                pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + 2, Y*PW), (PW - 4, 2)))
            if cell[1]:
                pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + (PW - 2), Y*PW + 2), (2, PW - 4)))
            if cell[2]:
                pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + 2, Y*PW + (PW - 2)), (PW - 4, 2)))
            if cell[3]:
                pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW, Y*PW + 2), (2, PW - 4)))
    return surf

############ MAIN LOOP #############
x, y = 0, 0
mazes = [breadth_first(), depth_first()]
maze, ent, ext, route = mazes.pop(0)
show = False
zoom = [8, 16, 32, 64]
zidx = 1
img = drawn_maze(maze, ent, ext)
rimg = drawn_maze(maze, ent, ext, route=route )
while True:
    if PW != zoom[zidx]:
        PW = zoom[zidx]
        img = drawn_maze(maze, ent, ext)
        rimg = drawn_maze(maze, ent, ext, route=route )
    SCREEN.fill((0, 0, 0))
    if show:
        SCREEN.blit(rimg, (x*PW, y*PW))
    else:
        SCREEN.blit(img, (x*PW, y*PW))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == QUIT: quit()
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                x -= 1
            if e.key == K_LEFT:
                x += 1
            if e.key == K_UP:
                y += 1
            if e.key == K_DOWN:
                y -= 1

            if e.key == K_z:
                zidx = (zidx + 1) % 4
            if e.key == K_x:
                zidx = (zidx - 1) % 4

            if e.key == K_n:
                if not mazes: quit()
                maze, ent, ext, route = mazes.pop(0)
                img = drawn_maze(maze, ent, ext)
                rimg = drawn_maze(maze, ent, ext, route=route )
            if e.key == K_SPACE:
                show = (show + 1) % 2
