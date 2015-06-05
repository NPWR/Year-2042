import pygame as pg
pg.font.init()

class ProgressBar:
    def __init__(self,size,lenght,color,title,maximum):
        self.title = title #Title next to the bar
        self.font = pg.font.Font('hollowpoint.ttf',size)
        self.sf = self.font.render(self.title,True,self.c)
        
        self.W = lenght
        self.progress = 100 #Percent
        self.count = maximum
        self.max = maximum

    def refreshProgress(self):
        self.progress = int(self.count*100/self.max)

    def sub(self,n):
        self.count -= n
        if self.count < 0:
            self.count = 0
        self.refreshProgress()
    
    def add(self,n):
        self.count += n
        if self.count > self.maximum:
            self.count = self.maximum
        self.refreshProgress()

    def draw(self,SF,pos,corner):
        """if corner == 'ul':
            tp =
            bp =
        if corner == 'ur':
            tp =
            bp =
        if corner == 'bl':
            tp =
            bp =
        if corner == 'br':
            tp =
            bp ="""
        

        
        
        
