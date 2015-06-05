from data import *
import gc
gc.enable()

if FULLSCREEN:
    WIN = pg.display.set_mode(WINSIZE,FULLSCREEN)
else:
    WIN = pg.display.set_mode(WINSIZE)

WORLD = Scene(10,5)
M_MASK = 0

while 1:
    WIN.fill(FILLCOLOR)
    
    for event in pg.event.get():
        M_MASK = handleEvent(WORLD,event, M_MASK)

    if KEY_ON["DOWN"]:
        WORLD.player.normalMove(PI/2.,CM)
    if KEY_ON["UP"]:
        WORLD.player.normalMove(-PI/2.,CM)
    if KEY_ON["LEFT"]:
        WORLD.player.normalMove(PI,CM)
    if KEY_ON["RIGHT"]:
        WORLD.player.normalMove(0,CM)
    if KEY_ON["LCLICK"]:
        WORLD.player.shoot()
    if KEY_ON["SPACE"]:
        pass
    if KEY_ON["RCLICK"]:
        WORLD.player.followMouse()

    WORLD.player.move()
    WORLD.followPlayer()
    WORLD.move()
    WORLD.player.rocketParticles.stop()
    WORLD.draw(WIN)
    pg.display.flip()

    pg.time.wait(WTT)
