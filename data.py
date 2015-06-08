from genericFunctions import *
import pygame as pg
from pygame.locals import *
from pygame import gfxdraw
from math import *
from random import randrange
import sys
PI = pi

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

        self.surfaces = []
        for j,plane in enumerate(self.planes):
            
            i = (self.depth-1)-j
            c = int((255/self.depth) * (self.depth - i))         
            c = (c,c,c)
            
            newSF = pg.Surface((W*2,H*2))
            smlSF = pg.Surface((W,H))
            
            for star in plane:
                pg.draw.circle(smlSF,c,star,2)
                pg.gfxdraw.aacircle(smlSF,star[0],star[1],2,c)

            newSF.blit(smlSF,(0,0))
            newSF.blit(smlSF,(W,0))
            newSF.blit(smlSF,(0,H))
            newSF.blit(smlSF,(W,H))

            newSF.set_colorkey((0,0,0),pg.RLEACCEL)

            self.surfaces.append(newSF)
        self.surfaces.reverse()

    def draw(self,SF,camPos):
        for i,surface in enumerate(self.surfaces):
            dmod = (i+1)*(i+1)
            pos = (int(camPos[0]/dmod),int(camPos[1]/dmod))

            x = pos[0] % W
            y = pos[1] % H
            rct = ((x,y),(W,H))

            SF.blit(surface,(0,0),rct)

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

        try:
            pg.gfxdraw.aacircle(SF,pos[0],pos[1],4,self.c)
        except:
            pass
        
        

class Spaceship:
    def __init__(self,pos):
        self.pos = pos
        self.vpos = [float(pos[0]),float(pos[1])]
        self.dx, self.dy =  0.,0.
        self.c = (255,255,255)
        self.c1 = (0,0,0)
        self.ang = 0.
        self.bullets = []
        self.fuel = MAX_FUEL_1

        self.readyToShoot = True
        self.levelCoolDown = 10
        self.coolDownTime = 0

        self.rocketParticles = ParticleSystem(ROCKET_COLOR,ROCKET_COLOR_VAR,ROCKET_LS,ROCKET_LS_VAR,ROCKET_MINSIZE,ROCKET_MAXSIZE)
        self.boosterParticles = ParticleSystem(BOOSTER_COLOR,BOOSTER_COLOR_VAR,BOOSTER_LS,BOOSTER_LS_VAR,BOOSTER_MINSIZE,BOOSTER_MAXSIZE)
        self.boosterParticles.setDrag(1.0)
        self.rocketParticles.setDrag(DRAG)
        
        self.shootAng = 0.

        self.growth = 1.0

        self.HP = MAX_HP_1

        self.bodySize = int(10*self.growth)
        self.rearSize = int(4*self.growth)

    def followMouse(self):
        self.normalMove(self.shootAng + PI,CM)

    def addFuel(self,UI):
        self.fuel += FUEL_VALUE

    def boost(self):
        if self.fuel >= 10:
            x = cos(self.ang + PI) * BOOST_SPEED
            y = sin(self.ang + PI) * BOOST_SPEED
            self.addMov([x,y])
            self.boosterParticles.start(BOOSTER_FLUX,1)
            self.fuel -= 10

    def normalMove(self,angle,speed):
        if self.fuel:
            x = cos(angle) * speed
            y = sin(angle) * speed
            vec = [x,y]
            self.addMov(vec)
            self.rocketParticles.start(ROCKET_FLUX)
            self.fuel -= 1

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

        

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
        pmx = cos(mang)* 30
        pmy = sin(mang)* 30
        self.rocketParticles.actuate(self.pos,[self.dx,self.dy],[pmx,pmy],ROCKET_SPREAD)
        self.boosterParticles.actuate(self.pos,[self.dx,self.dy],[pmx*2,pmy*2],BOOSTER_SPREAD)

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def draw(self,SF,camPos):
        #Particles drawing
        self.rocketParticles.draw(SF,camPos)
        self.boosterParticles.draw(SF,camPos)
        
        #Calculating screen pos
        pos = [self.pos[0]-camPos[0],self.pos[1]-camPos[1]]

        #Ship Drawing
        ang1 = self.ang + PI/4.
        ang2 = self.ang - PI/4.
        
        bodySize = int(10*self.growth)
        rearSize = int(4*self.growth)
        self.bodySize = bodySize
        self.rearSize = rearSize
        
        p1 = (int(pos[0] + cos(ang1)*bodySize), int(pos[1] + sin(ang1)*bodySize))
        p2 = (int(pos[0] + cos(ang2)*bodySize), int(pos[1] + sin(ang2)*bodySize))

        pg.gfxdraw.aacircle(SF,p1[0],p1[1],rearSize,self.c)
        pg.gfxdraw.aacircle(SF,p2[0],p2[1],rearSize,self.c)
        
        pg.draw.circle(SF,self.c1,pos,bodySize)
        pg.gfxdraw.aacircle(SF,pos[0],pos[1],bodySize,self.c)

        #Gun Drawing
        Ang = self.shootAng + PI
        sx, sy = int(cos(Ang)*4 + pos[0]) , int(sin(Ang)*rearSize + pos[1])
        ex, ey = int(cos(Ang)*8 + pos[0]) , int(sin(Ang)*rearSize*2 + pos[1])
        pg.draw.aaline(SF,ROCKET_COLOR,(sx,sy),(ex,ey))
        pg.gfxdraw.aacircle(SF,pos[0],pos[1],rearSize,ROCKET_COLOR)

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

        self.playerCell = [0,0]
        self.cellStackTest = {}
        self.cellStack = {}
        self.genFuel()

        self.previousCell = [0,0]

        self.UI = {}

    def addMov(self,vec):
        self.dx += vec[0]
        self.dy += vec[1]

    def genFuel(self):
        """
        Using dict for fuel cell notation:
        fuel = {"x":x,
                "y":y,
                "dx":dx,
                "dy":dy}
        """
        for nb in AROUND:
            cell = MOVE(self.playerCell,nb)
            key = str(cell[0])+":"+str(cell[1])
            been = False
            try:
                been = self.cellStackTest[key]
            except:
                been = False

            if not been:
                fuel = []
                for i in range(FUEL_PER_CELL):
                    x = randrange(W)
                    y = randrange(H)
                    c = {'x':x, 'y':y, 'dx':0., 'dy':0.}
                    fuel.append(c)
                self.cellStack[key] = fuel
                self.cellStackTest[key] = True
                

    def redefCell(self):
        x = int(floor(self.player.pos[0] / W))
        y = int(floor(self.player.pos[1] / H))

        self.playerCell = [x,y]

        if self.playerCell != self.previousCell:
            self.previousCell = self.playerCell
            self.genFuel()

    def moveFuelCells(self):
        for nb in AROUND:
            cell = MOVE(self.playerCell, nb)
            key = str(cell[0])+':'+str(cell[1])
            for fuel in self.cellStack[key]:
                fuel['x'] += fuel['dx']
                fuel['y'] += fuel['dy']
                fuel['dx'] *= DRAG
                fuel['dy'] *= DRAG
    

    def checkFuelCellsAttraction(self):
        for nb in AROUND:
            cell = MOVE(self.playerCell,nb)
            key = str(cell[0])+':'+str(cell[1])

            for i,fuel in enumerate(self.cellStack[key]):
                x = (cell[0] * W + fuel['x']) - self.pos[0]
                y = (cell[1] * H + fuel['y']) - self.pos[1]

                if onScreen((x,y)):
                    dx = x - CNTR[0]
                    dy = y - CNTR[1]
                    d = hypot(dx,dy)

                    if d <= FUEL_MAGNET_RANGE:
                        g = FUEL_MAGNET_STRENGHT/(d)
                        ang = atan2(dy,dx) + PI
                        x = cos(ang)*g
                        y = sin(ang)*g
                        fuel['dx'] += x
                        fuel['dy'] += y

                    if d <= self.player.bodySize*2:
                        self.player.addFuel(self.UI['XP'])
                        self.cellStack[key].pop(i)
    
    def refreshUI(self):
        self.UI['FUEL'].setCount(self.player.fuel)

    def move(self):
        self.vpos[0] += self.dx
        self.vpos[1] += self.dy
        self.dx *= DRAG
        self.dy *= DRAG
        self.actPos()
        self.redefCell()
        self.checkFuelCellsAttraction()
        self.moveFuelCells()
        self.refreshUI()

    def addUI(self,key,ui):
        self.UI[key] = ui
    
    def followPlayer(self):
        self.vpos[0] = self.player.vpos[0] - CNTR[0]
        self.vpos[1] = self.player.vpos[1] - CNTR[1]

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def drawFuel(self,SF,cp):
        for nb in AROUND:
            cell = MOVE(self.playerCell,nb)
            key = str(cell[0])+":"+str(cell[1])
            for fp in self.cellStack[key]:
                dx = cell[0] * W
                dy = cell[1] * H
                pos = (int((fp['x']+ dx)-cp[0]),int((fp['y']+dy)-cp[1]))
                if onScreen(pos):
                    pg.draw.circle(SF,(0,0,0),pos,FUEL_SIZE)
                    pg.gfxdraw.aacircle(SF,pos[0],pos[1],FUEL_SIZE,FUEL_COLOR)
                    pg.gfxdraw.aacircle(SF,pos[0],pos[1],int(FUEL_SIZE/2.),FUEL_COLOR)

    def drawUI(self,SF):
        for i,key in enumerate(self.UI):
            self.UI[key].draw(SF,UI_POS,i)

    def draw(self,SF):
        self.background.draw(SF,self.pos)
        self.drawFuel(SF,self.pos)
        self.player.draw(SF,self.pos)
        self.drawUI(SF)


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
         "SIZE":s,
         "BSIZE":s}
        """

        self.time = 0
        self.stopTime = 0
        self.spawnRate = 0

        self.DRAG = 1.0

    def setDrag(self,drag):
        self.DRAG = drag
        
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
            particle["Dx"] *= self.DRAG
            particle["Dy"] *= self.DRAG
            particle["AGE"] += 1
            particle["SIZE"] = int((float(particle["BSIZE"])/float(self.baseLifespan))*(float(self.baseLifespan)-float(particle["AGE"])))
            if particle["SIZE"] < 1:
                particle["SIZE"] = 1
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
                spd = hypot(pmov[0],pmov[1]) * (randrange(50,100)/100.)
                nAngle = oAngle + angleDev

                dx = cos(nAngle) * spd
                dy = sin(nAngle) * spd
                
                newP["Px"] = opos[0]
                newP["Py"] = opos[1]
                newP["Dx"] = omov[0] + dx
                newP["Dy"] = omov[1] + dy
                newP["AGE"] = 0
                newP["COLOR"] = verifyColor((r,g,b))
                newP["SIZE"] = randrange(self.minSize,self.maxSize)
                newP["BSIZE"] = newP["SIZE"]

                self.particles.append(newP)

        self.time += 1

    def draw(self,SF,cP):
        for p in self.particles:
            pos = (int(p["Px"])-cP[0],int(p["Py"])-cP[1])
            pg.draw.circle(SF,p["COLOR"],pos,p["SIZE"])
            
            
            
        
