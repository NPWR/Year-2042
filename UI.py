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

    def setMax(self,n):
        self.max = n
        self.refreshProgress()

    def setProgress(self,n):
        self.progress = n
        self.count = int(n*self.max/100.)

    def setCount(self,n):
        self.count = n
        if self.count < 0:
            self.count = 0
        if self.count > self.max:
            self.count = self.max
        self.refreshProgress()

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

    def draw(self,SF,corner,order):
        spc = 10
        if corner == 'ul':
            tp = (UI_MARGIN +  UI_BAR_W + spc, UI_MARGIN + (order*(UI_BAR_H+spc)))
            bp = (UI_MARGIN, UI_MARGIN + (order * (UI_BAR_H+spc)))
            
        if corner == 'ur':
            tp = (W - UI_BAR_W - UI_MARGIN - self.sf.get_width() - spc, UI_MARGIN + (order*(UI_BAR_H+spc)))
            bp = (W - UI_BAR_W - UI_MARGIN, UI_MARGIN + (order*(UI_BAR_H+spc)))
            
        if corner == 'bl':
            tp = (UI_MARGIN + UI_BAR_W, H - UI_MARGIN - (order*(UI_BAR_H+spc)))
            bp = (UI_MARGIN, H - UI_MARGIN - (order*(UI_BAR_H+spc)))
            
        if corner == 'br':
            tp = (W - UI_MARGIN - UI_BAR_W - self.sf.get_width(), H - UI_MARGIN - (order*(UI_BAR_H+spc)))
            bp = (W - UI_MARGIN - UI_BAR_W, H - UI_MARGIN - (order*(UI_BAR_H+spc)))

        SF.blit(self.sf,tp)

        rct = (bp,(UI_BAR_W,UI_BAR_H))
        progrect  = (bp,(int(self.progress*100./UI_BAR_W),UI_BAR_H))
        pg.draw.rect(SF, self.c,rct, 1)
        pg.draw.rect(SF, self.c,progrect)

class UpgradeSelection:
    def __init__(self,level):
        self.H = UPG_UI_H
        self.W = UPG_UI_W

        self.font = pg.font.Font('hollowpoint.ttf',30)
        self.uptxt =  self.font.render('Level Up !',True,(255,255,255))
        self.downtxt =  self.font.render('Choose an upgrade',True,(255,255,255))

        self.outlineC = UPG_UI_OUTLINE_COLOR
        self.fillC = UPG_UI_FILL_COLOR

        self.rects = [((25,75),(150,150)),
                     ((200,75),(150,150)),
                     ((375,75),(150,150))]

        self.clickZones = [((25,75),(175,225)),
                          ((200,75),(350,225)),
                          ((375,75),(525,225))]

        self.SF = self.initSurface()

        self.active = False
        self.timer = 0

    def initSurface(self):
        SF = pg.Surface((self.W, self.H))
        SF.fill(self.fillC)
        pg.draw.rect(SF, self.outlineC,((0,0),(self.W,self.H)),1)
        for zone in self.rects:
            pg.draw.rect(SF,self.outlineC,zone,1)

        tp = (self.W/2 - self.uptxt.get_width()/2, 75/2 - self.uptxt.get_height()/2)
        SF.blit(self.uptxt,tp)

        tp = (self.W/2 - self.downtxt.get_width()/2, (225+75/2) - self.downtxt.get_height()/2)
        SF.blit(self.downtxt,tp)

        return SF

    def appear(self):
        if not self.active:
            self.active = True

    def disappear(self):
        if self.active:
            self.timer += 1

            

    def upgradeChoice(self):
        mpos = pg.mouse.get_pos()
        pos = (mpos[0] - (W/2 - self.W/2), mpos[1] - (H/2 - self.H/2))

        choice = None
        for i,zone in enumerate(self.clickZones):
            if pos[0] >= zone[0][0] and pos[0] <= zone[1][0] and pos[1] >= zone[0][1] and pos[1] <= zone[1][1]:
                choice = i
        if choice != None:
            self.disappear()
        return choice

    def draw(self,SF):
        if self.active:
            if self.timer < UPG_UI_ANIM_TIME:
                ymax = H/2 - self.H/2
                y = int(self.timer*ymax/UPG_UI_ANIM_TIME)
                alpha = int(self.timer*255/UPG_UI_ANIM_TIME)
                pos = (W/2 - self.W/2,y)
                self.SF.set_alpha(alpha)
                SF.blit(self.SF, pos)

                self.timer += 1

            if self.timer == UPG_UI_ANIM_TIME:
                self.SF.set_alpha(255)
                pos = (W/2 - self.W/2, H/2 - self.H/2)
                SF.blit(self.SF,pos)
            
            if self.timer > UPG_UI_ANIM_TIME:
                ymax = H/2-self.H/2
                y = int((self.timer-UPG_UI_ANIM_TIME)*ymax/UPG_UI_ANIM_TIME) + (H/2-self.H/2)
                alpha = int((UPG_UI_ANIM_TIME*2 - self.timer)*255/UPG_UI_ANIM_TIME)
                pos = (W/2 - self.W/2,y)
                self.SF.set_alpha(alpha)
                SF.blit(self.SF, pos)

                self.timer += 1

                if self.timer >= UPG_UI_ANIM_TIME*2:
                    self.active = False
                    self.timer = 0
    
        
        
        
