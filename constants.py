from math import pi

H = 768
W = 1368
WINSIZE = (W,H)
FULLSCREEN = True

CenterX = W/2
CenterY = H/2
CNTR = (CenterX,CenterY)

FRAMERATE = 60
WTT = int(1000./float(FRAMERATE))

FILLCOLOR = (0,0,0) #Bckground color

DRAG = 0.9

CM = 2.5 #Player acceleration in pxl/frame

BULLET_SPEED = 20. #Bullet Speed in pxl/frame
BULLET_LS = 180 #Bullet lifespan in frames

KEY_ON = {
    "UP":False,
    "DOWN":False,
    "LEFT":False,
    "RIGHT":False,
    "SPACE":False,
    "LCLICK":False}

ROCKET_COLOR = (0,120,255)
ROCKET_COLOR_VAR = 25
ROCKET_LS = 10
ROCKET_LS_VAR = 5
ROCKET_MINSIZE = 4
ROCKET_MAXSIZE = 8
ROCKET_SPREAD = pi/16.
ROCKET_FLUX = 10

BOOST_SPEED = 20.

BOOSTER_COLOR = (255,100,50)
BOOSTER_COLOR_VAR = 25
BOOSTER_LS = 11
BOOSTER_LS_VAR = 10
BOOSTER_MINSIZE = 5
BOOSTER_MAXSIZE = 6
BOOSTER_SPREAD = pi/8.

