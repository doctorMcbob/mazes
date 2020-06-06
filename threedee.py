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
PW = 32
W, H, L = 10, 10, 10

ENT = (randint(0, W-1), randint(0, H-1), randint(0, L-1))
EXT = None

SCREEN = pygame.display.set_mode((PW * 20, PW * 20))
pygame.display.set_caption("take advantage of your spacial dimension")

def get(Q, X, Y, Z): return Q[Z][Y][X]

# algorithm

def first_draft():
    Q = blank()
    routes = {ENT: [ENT]}
    heads = [ENT]
    marked = []
    counter = (W + H + L) // 3
    while heads or len(marked) < (W*H)/2:
        if not heads: heads.append(coice(marked))
        if counter <= 0:
            counter = (W+H+L)//3
            shuffle(heads)
        x, y, z = heads.pop()
        debug(Q, (x, y, z))
        route = routes[(x, y, z)]
        exits = get(Q, x, y, z)

        n = choice([2, 2, 3, 4, 5, 6])
        while sum(exits) < n: get(Q, x, y, z)[randint(0, 5)] = 1
        for d, check in enumerate(exits):
            if check:
                x_, y_, z_ = apply_direction(x, y, z, d)
                if W > x_ >= 0 and H > y_ >= 0 and L > z_ >= 0:
                    if (x_, y_, z_) not in heads and (x_, y_, z_) not in marked:
                        get(Q, x_, y_, z_)[direction_inverse(d)] = 1
                        heads.append((x_, y_, z_))
                        routes[(x_, y_, z_)] = route + [(x_, y_, z_)]
                    elif get(Q, x_, y_, z_)[direction_inverse(d)] == 0:
                        get(Q, x, y, z)[d] = 0
                        counter -= 1
                else:
                    get(Q, x, y, z)[d] = 0
                    counter -= 1
        marked.append((x, y, z))
    return Q, routes

def second_draft():
    Q = blank()
    routes = {ENT: [ENT]}
    heads = [ENT]
    marked = []
    counter = (W + H + L) // 3
    while heads or len(marked) < (W*H)/2:
        if not heads: heads.append(coice(marked))
        if counter <= 0:
            counter = (W+H+L)//3
            shuffle(heads)
        x, y, z = heads.pop()
        debug(Q, (x, y, z))
        route = routes[(x, y, z)]
        exits = get(Q, x, y, z)

        n = choice([2, 2, 3, 4])
        roll = randint(0, 100)
        if roll >= 94: exits[4] = 1
        elif roll <= 5: exits[5] = 1
        while sum(exits[:-2]) < n: get(Q, x, y, z)[randint(0, 3)] = 1
        for d, check in enumerate(exits):
            if check:
                x_, y_, z_ = apply_direction(x, y, z, d)
                if W > x_ >= 0 and H > y_ >= 0 and L > z_ >= 0:
                    if (x_, y_, z_) not in heads and (x_, y_, z_) not in marked:
                        get(Q, x_, y_, z_)[direction_inverse(d)] = 1
                        heads.append((x_, y_, z_))
                        routes[(x_, y_, z_)] = route + [(x_, y_, z_)]
                    elif get(Q, x_, y_, z_)[direction_inverse(d)] == 0:
                        get(Q, x, y, z)[d] = 0
                        counter -= 1
                else:
                    get(Q, x, y, z)[d] = 0
                    counter -= 1
        marked.append((x, y, z))
    return Q, routes
    
    
def apply_direction(X, Y, Z, d):
    return X + [0, 1, 0, -1, 0, 0][d], Y + [-1, 0, 1, 0, 0, 0][d], Z + [0, 0, 0, 0, -1, 1][d]
def direction_inverse(d): return {0:2, 1:3, 2:0, 3:1, 4:5, 5:4}[d]

def blank():
    Q = []
    for Z in range(L):
        Q.append([])
        for Y in range(H):
            Q[-1].append([])
            for X in range(W):
                Q[-1][-1].append([0, 0, 0, 0, 0, 0])
    return Q

def debug(Q, pos, pause=False):
    SCREEN.blit(draw(Q, pos[-1], route=[pos]), (0, 0))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == QUIT: quit()
    while pause:
        for e in pygame.event.get():
            if e.type == QUIT: quit()
            if e.type == KEYDOWN and e.key == K_SPACE: pause = False

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
            if sum(spot): pygame.draw.rect(surf, col, pygame.rect.Rect((X*PW + PW/8, Y*PW + PW/8), (PW - (PW/8)*2, PW - (PW/8)*2)))
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

def solve():
    global EXT
    for Q, routes in [first_draft(), second_draft()]:
        EXT = ENT
        for route in routes:
            if len(routes[route]) > len(routes[EXT]):
                EXT = route
        X, Y, Z = ENT
        while (X, Y, Z) != EXT:
            mov = [0, 0, 0]
            for e in pygame.event.get():
                if e.type == QUIT: quit()
                if e.type == KEYDOWN:
                    if e.key == K_UP: mov[1] = -1
                    if e.key == K_DOWN: mov[1] = 1
                    if e.key == K_LEFT: mov[0] = 1
                    if e.key == K_RIGHT: mov[0] = -1
                    if e.key == K_z: mov[2] = -1
                    if e.key == K_x: mov[2] = 1
            spot = get(Q, X, Y, Z)
            if mov[1] < 0 and spot[0]: Y -= 1
            if mov[1] > 0 and spot[2]: Y += 1
            if mov[0] > 0 and spot[3]: X -= 1
            if mov[0] < 0 and spot[1]: X += 1
            if mov[2] > 0 and spot[4]: Z -= 1
            if mov[2] < 0 and spot[5]: Z += 1
            SCREEN.fill((50, 50, 50))
            SCREEN.blit(draw(Q, Z, route=routes[EXT]), ((((SCREEN.get_width() / PW) // 2) - X) * PW, (((SCREEN.get_height() / PW) // 2) - Y) * PW))

            surf = pygame.Surface((PW-(PW/8)*2, PW-(PW/8)*2))
            surf.fill((255, 0, 255))
            surf.set_alpha(128)
            SCREEN.blit(surf, (((SCREEN.get_width() // PW) // 2) * PW + PW/8, ((SCREEN.get_height() / PW) // 2) * PW + PW/8))
            pygame.display.update()

if __name__ == "__main__":
    solve()
