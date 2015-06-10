import pygame as pg
from pygame.locals import *
from constants import *
import sys

AROUND = [[0,0],
          [1,0],
          [1,1],
          [0,1],
          [-1,1],
          [-1,0],
          [-1,-1],
          [0,-1],
          [1,-1]]

def MOVE(cell,vec):
    return [cell[0]+vec[0],cell[1]+vec[1]]

KEY_ON = {
    "UP":False,
    "DOWN":False,
    "LEFT":False,
    "RIGHT":False,
    "SPACE":False,
    "LCLICK":False,
    "RCLICK":False}

def onScreen(pos):
    ret = True
    if pos[0] < 0:
        ret = False
    elif pos[0] >= W:
        ret = False
    if pos[1] < 0:
        ret = False
    elif pos[1] >= H:
        ret = False

    return ret

def verifyColor(color):
    r = color[0]
    g = color[1]
    b = color[2]

    if r < 0:
        r = 0
    elif r > 255:
        r = 255

    if g < 0:
        g = 0
    elif r > 255:
        g = 0

    if b < 0:
        b = 0
    elif b > 255:
        b = 255

    return (r,g,b)


def handleEvent(WORLD,event,M_MASK):
    mb = pg.mouse.get_pressed()
    N_MASK = 0
    if mb[0]:
        N_MASK += M_L
    if mb[1]:
        N_MASK += M_M
    if mb[2]:
        N_MASK += M_R

    D_MASK = -(N_MASK - M_MASK)
    M_MASK = N_MASK
    
    if event.type == QUIT:
            pg.quit()
            sys.exit()
    if event.type == KEYDOWN:
        if event.key == K_F4:
            pg.quit()
            sys.exit()
            
        if event.key == K_DOWN or event.key == K_s:
            KEY_ON["DOWN"] = True

        if event.key == K_UP or event.key == K_w:
            KEY_ON["UP"] = True
            
        if event.key == K_LEFT or event.key == K_a:
            KEY_ON["LEFT"] = True
            
        if event.key == K_RIGHT or event.key == K_d:
            KEY_ON["RIGHT"] = True
            
        if event.key == K_SPACE:
            KEY_ON["SPACE"] = True

    if event.type == MOUSEBUTTONDOWN:
        if pg.mouse.get_pressed()[0]:
            KEY_ON["LCLICK"] = True
        if pg.mouse.get_pressed()[2]:
            KEY_ON["RCLICK"] = True
    
    else:
        if D_MASK & M_R:
            KEY_ON["RCLICK"] = False
        if D_MASK & M_L:
            KEY_ON["LCLICK"] = False
            

    if event.type == KEYUP:
        if event.key == K_DOWN or event.key == K_s:
            KEY_ON["DOWN"] = False

        if event.key == K_UP or event.key == K_w:
            KEY_ON["UP"] = False

        if event.key == K_LEFT or event.key == K_a:
            KEY_ON["LEFT"] = False

        if event.key == K_RIGHT or event.key == K_d:
            KEY_ON["RIGHT"] = False

        if event.key == K_SPACE:
            KEY_ON["SPACE"] = False
            
    return M_MASK
