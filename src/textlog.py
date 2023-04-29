import object

class textLog(object):
    _logList = []
    _screenColor = (0, 0, 0)

    def __init__(self, pos, scene, f, c = (255,255,255), sc = (0,0,0), ml = 15,s = 7, grad = True, utd = True) -> None:
        super().__init__(pos,scene)
        self._font = f
        self._mainColor = c 
        self._maxLength = ml
        self._screenColor = sc
        self._gradation = grad
        self._upToDown = utd
        self._size = s
        self._fontSize = self._font.size("가")

    def addLine(self,s):
        self._logList.insert(0,s)
        if len(self._logList) > self.size:
            self._logList.pop()

    def draw(self):
        color = self._mainColor
        l = self.size
        for i in range(len(self._logList)):
            if self._gradation:
                color = (self._mainColor[0]*(l-i)/l,self._mainColor[1]*(l-i)/l,self._mainColor[2]*(l-i)/l)
            text = self._font.render(self._logList[i], True, color, self._screenColor)
            if self._upToDown:
                self.getScreen().blit(text, (self._pos[0],self._pos[1]+i*self._fontSize[1]))
            else:
                self.getScreen().blit(text, (self._pos[0],self._pos[1]-(i+1)*self._fontSize[1]))
