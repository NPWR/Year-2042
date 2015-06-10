import math as m
from constants import *

class rigidBody:
    def __init__(self,pos,d = [0.,0.]):
        self.ang = 0.
        self.pos = pos
        self.d = d
        self.vpos = [float(pos[0]),float(pos[1])]

    def actPos(self):
        self.pos = (int(self.vpos[0]),int(self.vpos[1]))

    def move(self):
        self.vpos[0] += self.d[0]
        self.vpos[1] += self.d[1]
        self.actPos()

        self.d[0] *= DRAG
        self.d[1] *= DRAG

    def addMov(self,vec):
        self.d[0] += vec[0]
        self.d[1] += vec[1]
    
