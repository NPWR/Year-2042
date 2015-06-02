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

CM = 7.5 #Player acceleration in pxl/frame

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
ROCKET_LS = 5
ROCKET_LS_VAR = 1
ROCKET_MINSIZE = 4
ROCKET_MAXSIZE = 8
ROCKET_SPREAD = pi/12.
ROCKET_FLUX = 10

BOOST_SPEED = 200.

BOOSTER_COLOR = (245,48,240)
BOOSTER_COLOR_VAR = 50
BOOSTER_LS = 20
BOOSTER_MINSIZE = 1
BOOSTER_MAXSIZE = 5
BOOSTER_SPREAD = pi/6.

