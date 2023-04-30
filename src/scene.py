class scene:
    _objects = dict()
    _screen = None
    def __init__(self,s):
        self._screen = s

    def addObj(self,obj):
        self._objects[obj.getId()] = obj

    def delObj(self,obj):
        del(self._objects[obj.getId()])
    
    def draw(self):
        for id in self._objects:
            obj = self._objects[id]
            obj.draw()

    def getScreen(self):
        return self._screen