class textLog:
    logList = []
    screenColor = (0, 0, 0)

    def __init__(self, f, c = (255,255,255), sc = (0,0,0), ml = 15,s = 7, grad = True, utd = True) -> None:
        self.font = f
        self.mainColor = c 
        self.maxLength = ml
        self.screenColor = sc
        self.gradation = grad
        self.upToDown = utd
        self.size = s
        self.fontSize = self.font.size("가")

    def addLine(self,s):
        self.logList.insert(0,s)
        if len(self.logList) > self.size:
            self.logList.pop()

    def draw(self, screen, pos):
        color = self.mainColor
        l = self.size
        for i in range(len(self.logList)):
            if self.gradation:
                color = (self.mainColor[0]*(l-i)/l,self.mainColor[1]*(l-i)/l,self.mainColor[2]*(l-i)/l)
            text = self.font.render(self.logList[i], True, color, self.screenColor)
            if self.upToDown:
                screen.blit(text, (pos[0],pos[1]+i*self.fontSize[1]))
            else:
                screen.blit(text, (pos[0],pos[1]-(i+1)*self.fontSize[1]))
