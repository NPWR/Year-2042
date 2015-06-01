from constants import *
import pygame as pg
from pygame.locals import *
from pygame import gfxdraw
from math import *
from random import randrange
import sys
PI = pi

def handleEvent(event):
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
            
    if event.type == MOUSEBUTTONUP:
        KEY_ON["LCLICK"] = False



class Background:
    def __init__(self,density,depth):
        self.density = density
        self.depth = depth
        self.initPlanes()

    def initPlanes(self):
        self.planes = []
        for i in range(self.depth):
            self.planes.append([])
            for j in range(self.density*((i+1)/2)+1):
                star = (randrange(W),randrange(H))
                self.planes[i].append(star)

    def draw(self,SF,camPos):
        for i,plane in enumerate(self.planes):
            c = int((255/self.depth) * (self.depth - i))         
            c = (c,c,c)
            
            for star in plane:
                dmod = (i+2)*(i+2)
                pos = [star[0]-camPos[0]/dmod,star[1]-camPos[1]/dmod]

                if pos[0]<0:
                    pos[0] = W - abs(pos[0]) % W
                if pos[0]>W:
                    pos[0] = 0 + abs(pos[0]) % W
                if pos[1]<0:
                    pos[1] = H - abs(pos[1]) % H
                if pos[1]>H:
                    pos[1] = 0 + abs(pos[1]) % H

                pos = (pos[0],pos[1])

                pg.gfxdraw.aacircle(SF,pos[0],pos[1],2,c)
                pg.draw.circle(SF,c,pos,2)

class Bullet:
    def __init__(self,pos,ang,d):
        self.ang = ang + PI
        self.pos = pos
        self.vpos = [float(pos[0]),float(pos[1])]
        self.dx, self.dy =  cos(self.ang) * BULLET_SPEED + d[0], sin(self.ang) * BULLET_SPEED + d[1]
        self.c = (255,255,255)
        self.c1 = (0,0,0)
        self.life = BULLET_LS

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

    def move(self):
        self.vpos[0] += self.dx
        self.vpos[1] += self.dy
        self.actPos()
        self.life -= 1

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def draw(self,SF,camPos):
        pos = (self.pos[0]-camPos[0],self.pos[1]-camPos[1])
        
        pg.gfxdraw.aacircle(SF,pos[0],pos[1],4,self.c)
        
        

class Spaceship:
    def __init__(self,pos):
        self.pos = pos
        self.vpos = [float(pos[0]),float(pos[1])]
        self.dx, self.dy =  0.,0.
        self.c = (255,255,255)
        self.c1 = (0,0,0)
        self.ang = 0.
        self.bullets = []

        self.readyToShoot = True
        self.levelCoolDown = 10
        self.coolDownTime = 0

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

    def redefAngle(self):
        """
        dx = self.dx
        dy = self.dy
        """
        dx = pg.mouse.get_pos()[0] - CNTR[0]
        dy = pg.mouse.get_pos()[1] - CNTR[1]

        ang = atan2(dy,dx) + PI
        self.ang = ang

    def coolDown(self):
        if self.coolDownTime > 0 and not self.readyToShoot:
            self.coolDownTime -= 1

        else:
            self.readyToShoot = True
    
    def shoot(self):
        if self.readyToShoot:
            self.bullets.append(Bullet(self.pos,self.ang,[self.dx,self.dy]))
            self.readyToShoot = False
            self.coolDownTime = self.levelCoolDown
    
    def move(self):
        self.vpos[0] += self.dx
        self.vpos[1] += self.dy
        self.dx *= DRAG
        self.dy *= DRAG
        self.actPos()
        self.redefAngle()
        for i,bullet in enumerate(self.bullets):
            bullet.move()
            if bullet.life  == 0:
                self.bullets.pop(i)

        self.coolDown()

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def draw(self,SF,camPos):
        pos = [self.pos[0]-camPos[0],self.pos[1]-camPos[1]]

        pg.gfxdraw.aacircle(SF,pos[0],pos[1],10,self.c)

        ang1 = self.ang + PI/4.
        ang2 = self.ang - PI/4.
        p1 = (int(pos[0] + cos(ang1)*10), int(pos[1] + sin(ang1)*10))
        p2 = (int(pos[0] + cos(ang2)*10), int(pos[1] + sin(ang2)*10))

        pg.gfxdraw.aacircle(SF,p1[0],p1[1],4,self.c)
        pg.gfxdraw.aacircle(SF,p2[0],p2[1],4,self.c)

        for bullet in self.bullets:
            bullet.draw(SF,camPos)


class Scene:
    def __init__(self):
        self.pos = (-CNTR[0],-CNTR[1])
        self.vpos = [0.,0.]
        self.dx, self.dy =  0.,0.
        self.viewSize = WINSIZE
        self.background = Background(10,5)
        self.player = Spaceship(self.pos)

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

    def move(self):
        self.vpos[0] += self.dx
        self.vpos[1] += self.dy
        self.dx *= DRAG
        self.dy *= DRAG
        self.actPos()

    def followPlayer(self):
        self.vpos[0] = self.player.vpos[0] - CNTR[0]
        self.vpos[1] = self.player.vpos[1] - CNTR[1]

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def draw(self,SF):
        self.background.draw(SF,self.pos)
        self.player.draw(SF,self.pos)
