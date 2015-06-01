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

CM = 5. #Player acceleration in pxl/frame

BULLET_SPEED = 20. #Bullet Speed in pxl/frame
BULLET_LS = 180 #Bullet lifespan in frames

KEY_ON = {
    "UP":False,
    "DOWN":False,
    "LEFT":False,
    "RIGHT":False,
    "SPACE":False,
    "LCLICK":False}
