from math import pi
from screenres import *

#Mouse buttons binary masks:
M_L, M_M, M_R = 1,2,4


#H = 768
#W = 1368
WINSIZE = (W,H)
FULLSCREEN = True

CenterX = W/2
CenterY = H/2
CNTR = (CenterX,CenterY)

FRAMERATE = 60
WTT = int(1000./float(FRAMERATE))

FILLCOLOR = (0,0,0) #Bckground color

DRAG = 0.9

CM = 2.0 #Player acceleration in pxl/frame

BULLET_SPEED = 20. #Bullet Speed in pxl/frame
BULLET_LS = 180 #Bullet lifespan in frames

KEY_ON = {
    "UP":False,
    "DOWN":False,
    "LEFT":False,
    "RIGHT":False,
    "SPACE":False,
    "LCLICK":False,
    "RCLICK":False}

FUEL_PER_CELL = 5

UI_MARGIN = 20
UI_BAR_H =  10
UI_BAR_W = 100

ROCKET_COLOR = (0,120,255)
ROCKET_COLOR_VAR = 25
ROCKET_LS = 10
ROCKET_LS_VAR = 5
ROCKET_MINSIZE = 4
ROCKET_MAXSIZE = 8
ROCKET_SPREAD = pi/16.
ROCKET_FLUX = 5

BOOST_SPEED = 40.

BOOSTER_COLOR = (255,50,50)
BOOSTER_COLOR_VAR = 25
BOOSTER_LS = 11
BOOSTER_LS_VAR = 10
BOOSTER_MINSIZE = 5
BOOSTER_MAXSIZE = 6
BOOSTER_SPREAD = pi/10.
BOOSTER_FLUX = 50

FUEL_SIZE = 4
FUEL_COLOR = (0,255,0)
FUEL_MAGNET_RANGE = 150
FUEL_MAGNET_STRENGHT = 200. #pxl/fr^2
FUEL_VALUE = 30

UI_POS = 'ur'

START_FUEL = 360

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

