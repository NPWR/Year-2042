from UI import *
import gc
gc.enable()

WORLD = Scene(10,5)
M_MASK = 0

XP_Bar = ProgressBar(18,100,(255,255,255),"XP",100)
XP_Bar.setProgress(0)
FUEL_Bar = ProgressBar(18,100,(255,255,255),"FUEL",MAX_FUEL_1)
HP_Bar = ProgressBar(18,100,(255,255,255),"HP",MAX_HP_1)
LVL_UP = UpgradeSelection(0)

WORLD.addUI('HP',HP_Bar)
WORLD.addUI('XP',XP_Bar)
WORLD.addUI('FUEL',FUEL_Bar)
WORLD.addUI('',LVL_UP,True)


WIN = pg.display.set_mode(WINSIZE,FULLSCREEN)

while 1:
    WIN.fill(FILLCOLOR)
    
    for event in pg.event.get():
        M_MASK = handleEvent(WORLD,event, M_MASK)

    if KEY_ON["DOWN"]:
        WORLD.signal('D')
    if KEY_ON["UP"]:
        WORLD.signal('U')
    if KEY_ON["LEFT"]:
        WORLD.signal('L')
    if KEY_ON["RIGHT"]:
        WORLD.signal('R')
    if KEY_ON["LCLICK"]:
        WORLD.signal('LCLICK')
    if KEY_ON["SPACE"]:
        WORLD.signal('SPACE')
    if KEY_ON["RCLICK"]:
        WORLD.signal('RCLICK')

    WORLD.player.actuate()
    WORLD.followPlayer()
    WORLD.move()
    WORLD.player.rocketParticles.stop()
    WORLD.draw(WIN)
    pg.display.flip()

    pg.time.wait(WTT)
