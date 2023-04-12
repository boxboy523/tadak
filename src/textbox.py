import pygame

class textBox:
    mainStr = ''
    #frontStr = ''
    color = (255,255,255)
    whiteBar = False
    def __init__(self, f, s='', fs='', c=(255,255,255)) -> None:
        self.font = f
        self.mainStr = s
        #self.frontStr =fs
        self.color = c

    def setStr(self,s):
        self.mainStr = s

    def getStr(self):
        return self.mainStr

    def getLen(self):
        return len(self.mainStr)
    
    def setColor(self,c):
        self.color = c

    def subStr(self,i):
        self.mainStr = self.mainStr[:len(self.mainStr)-i]

    def addStr(self,s):
        self.mainStr += s


    def drawBox(self,screen,pos):
        text = self.font.render(self.mainStr, True, self.color)
        pygame.draw.rect(screen, self.color, [pos[0],pos[1],300,self.font.size("a")[1]],4)
        screen.blit(text, pos)
    