from data import *

if FULLSCREEN:
    WIN = pg.display.set_mode(WINSIZE,FULLSCREEN)
else:
    WIN = pg.display.set_mode(WINSIZE)

WORLD = Scene(5,5)

while 1:
    WIN.fill(FILLCOLOR)
    
    for event in pg.event.get():
        handleEvent(event)

    if KEY_ON["DOWN"]:
        WORLD.player.addMov([0.,CM])
    if KEY_ON["UP"]:
        WORLD.player.addMov([0.,-CM])
    if KEY_ON["LEFT"]:
        WORLD.player.addMov([-CM,0.])
    if KEY_ON["RIGHT"]:
        WORLD.player.addMov([CM,0.])
    if KEY_ON["SPACE"] or KEY_ON["LCLICK"]:
        WORLD.player.shoot()

    WORLD.player.move()
    WORLD.followPlayer()
    WORLD.move()
    WORLD.player.rocketParticles.stop()
    WORLD.draw(WIN)
    pg.display.flip()

    pg.time.wait(WTT)
