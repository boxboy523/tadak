class object:
    _pos = (0,0)
    _scene = None
    _idCounter = 0
    _id = None
    def __init__(self, p, s):
        self._pos = p
        self._scene = s
        self._id = object._idCounter
        object._idCounter += 1
        s.addObj(self)

    def getId(self):
        return self._id

    def delete(self):
        self._scene.delObj(self)

    def movePos(self,dx,dy):
        self._pos = (self._pos[0]+dx,self._pos[1]+dy)

    def setPos(self,x,y):
        self._pos = (x,y)

    def getScreen(self):
        return self._scene.getScreen()

    def draw(self):
        pass