from UI import *
#from UI import *
import gc
gc.enable()

WIN = pg.display.set_mode(WINSIZE,FULLSCREEN)

WORLD = Scene(10,5)
M_MASK = 0

XP_Bar = ProgressBar(14,100,(255,255,255),"XP",100)

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
    XP_Bar.draw(WIN,'ur')
    pg.display.flip()

    pg.time.wait(WTT)
