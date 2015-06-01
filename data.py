from constants import *
import pygame as pg
from pygame.locals import *
from pygame import gfxdraw
from math import *
from random import randrange
import sys
PI = pi

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
            for j in range(self.density*(i+1)):
                star = (randrange(W),randrange(H))
                self.planes[i].append(star)
        self.planes.reverse()

    def draw(self,SF,camPos):
        for j,plane in enumerate(self.planes):
            i = (self.depth-1)-j
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

        self.rocketParticles = ParticleSystem((120,50,255),50,3,2,2,5)

        self.shootAng = 0.

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

        self.rocketParticles.start(10)

    def redefAngle(self):
        dx = self.dx
        dy = self.dy

        ang = atan2(dy,dx) + PI
        self.ang = ang

        dx = pg.mouse.get_pos()[0] - CNTR[0]
        dy = pg.mouse.get_pos()[1] - CNTR[1]

        ang = atan2(dy,dx) + PI
        self.shootAng = ang

    def coolDown(self):
        if self.coolDownTime > 0 and not self.readyToShoot:
            self.coolDownTime -= 1

        else:
            self.readyToShoot = True
    
    def shoot(self):
        if self.readyToShoot:
            self.bullets.append(Bullet(self.pos,self.shootAng,[self.dx,self.dy]))
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

        mang = atan2(self.dy,self.dx)
        pmx = cos(mang)* 10
        pmy = sin(mang)* 10
        self.rocketParticles.actuate(self.pos,[self.dx,self.dy],[pmx,pmy],PI/4)

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def draw(self,SF,camPos):
        self.rocketParticles.draw(SF,camPos)
        
        pos = [self.pos[0]-camPos[0],self.pos[1]-camPos[1]]
        
        pg.draw.circle(SF,self.c1,pos,10)
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
    def __init__(self,BgDensity,BgDepth):
        self.pos = (-CNTR[0],-CNTR[1])
        self.vpos = [0.,0.]
        self.dx, self.dy =  0.,0.
        self.viewSize = WINSIZE
        self.background = Background(BgDensity,BgDepth)
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


class ParticleSystem:
    def __init__(self, color, colorRange, medLs, varLs, minSize, maxSize):
        self.baseCol = color
        self.colorMod = colorRange

        self.baseLifespan = medLs
        self.lifespanVariation = varLs

        self.minSize = minSize
        self.maxSize = maxSize
        
        self.active = False
        self.particles = []
        """
        Particles are modelised by a dict:
        {"Px":x,
         "Py":y,
         "Dx":dx,
         "Dy":dy,
         "AGE":age,
         "COLOR":(r,g,b),
         "SIZE":s}
        """

        self.time = 0
        self.stopTime = 0
        self.spawnRate = 0
        
    def start(self,flux,stop = None):
        if not self.active:
            self.active = True
            self.time = 0
            if stop != None:
                self.stopTime = stop

            self.spawnRate = flux # particles/s

    def stop(self):
        if self.active:
            self.active = False
            self.time = 0
            self.stopTime = 0
            self.spawnRate = 0

    def actuate(self, opos, omov, pmov, spread):
        #Move existing particles and delete old ones
        toDel = []
        for i,particle in enumerate(self.particles):
            particle["Px"] += particle["Dx"]
            particle["Py"] += particle["Dy"]
            particle["Dx"] *= DRAG
            particle["Dy"] *= DRAG
            particle["AGE"] += 1

            rnd = randrange(-self.lifespanVariation,self.lifespanVariation)
            if particle["AGE"] > self.baseLifespan + rnd:
                toDel.append(i)

        toDel.reverse()
        for i in toDel:
            self.particles.pop(i)
                
        if self.active:
            #Stop the system if necessary
            if self.stopTime != 0:
                if self.time >= self.stopTime:
                    self.stop()
                    return 0

            #Spawn new particles
            for particle in range(self.spawnRate):
                newP = {}
                
                r = randrange(self.baseCol[0] - self.colorMod, self.baseCol[0] + self.colorMod)
                g = randrange(self.baseCol[1] - self.colorMod, self.baseCol[1] + self.colorMod)
                b = randrange(self.baseCol[2] - self.colorMod, self.baseCol[2] + self.colorMod)

                angleDev = int(degrees(spread)/2.)
                angleDev = randrange(-angleDev,angleDev)
                angleDev = radians(angleDev)

                oAngle = atan2(pmov[1],pmov[0]) + PI
                spd = hypot(pmov[0],pmov[1])
                nAngle = oAngle + angleDev

                dx = cos(nAngle) * spd
                dy = sin(nAngle) * spd
                
                newP["Px"] = opos[0]
                newP["Py"] = opos[1]
                newP["Dx"] = omov[0] + dx
                rndmod = randrange(90,120)/100.
                newP["Dx"] *= rndmod
                newP["Dy"] = omov[1] + dy
                rndmod = randrange(90,120)/100.
                newP["Dy"] *= rndmod
                newP["AGE"] = 0
                newP["COLOR"] = verifyColor((r,g,b))
                newP["SIZE"] = randrange(self.minSize,self.maxSize)

                self.particles.append(newP)

    def draw(self,SF,cP):
        for p in self.particles:
            pos = (int(p["Px"])-cP[0],int(p["Py"])-cP[1])
            pg.draw.circle(SF,p["COLOR"],pos,p["SIZE"])
            
            
            
        
