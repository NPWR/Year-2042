from data import *

pg.font.init()

class ProgressBar:
    def __init__(self,size,lenght,color,title,maximum):
        self.title = title #Title next to the bar
        self.font = pg.font.Font('hollowpoint.ttf',size)
        self.c = color
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

    def draw(self,SF,corner):
        if corner == 'ul':
            tp = (UI_MARGIN +  UI_BAR_W, UI_MARGIN)
            bp = (UI_MARGIN, UI_MARGIN)
            
        if corner == 'ur':
            tp = (W - UI_BAR_W - UI_MARGIN - self.sf.get_width(), UI_MARGIN)
            bp = (W - UI_BAR_W - UI_MARGIN, UI_MARGIN)
            
        if corner == 'bl':
            tp = (UI_MARGIN + UI_BAR_W, H - UI_MARGIN)
            bp = (UI_MARGIN, H - UI_MARGIN)
            
        if corner == 'br':
            tp = (W - UI_MARGIN - UI_BAR_W - self.sf.get_width(), H - UI_MARGIN)
            bp = (W - UI_MARGIN - UI_BAR_W, H - UI_MARGIN)

        SF.blit(self.sf,tp)

        rct = (bp,(UI_BAR_W,UI_BAR_H))
        progrect  = (bp,(int(self.progress*100./UI_BAR_W),UI_BAR_H))
        pg.draw.rect(SF, self.c,rct, 1)
        pg.draw.rect(SF, self.c,progrect)
        

        
        
        
