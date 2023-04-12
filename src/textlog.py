class textLog:
    logList = []
    screenColor = (0, 0, 0)

    def __init__(self, f, c = (255,255,255), sc = (0,0,0), ml = 15, grad = True, utd = True) -> None:
        self.font = f
        self.mainColor = c 
        self.maxLength = ml
        self.screenColor = sc
        self.gradation = grad
        self.upToDown = utd
        self.fontSize = self.font.size("가")

    def addLine(self,str):
        self.logList.append(str)

    def draw(self, screen, pos):
        for 