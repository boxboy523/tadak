import pygame

class keyClass:

    def __init__(self):
        self.keyAvailable = True
        self.pressedKey = set()
        self.keyFunction = dict()   

    def getKey(self,event):
        for e in event.get():
            if self.keyAvailable:
                break

            if e.type == pygame.KEYDOWN:
                self.pressedKey.add(e.key)
            
            if e.type == pygame.KEYUP:
                self.pressedKey.remove(e.key)
    
    def excuteKeyFunc(self):
        for key in self.pressedKey:
            try:
                self.keyFunction[key]()
                return None
            except:
                return key
    
    def setKeyFunc(self, key, func):
        self.keyFunction[key] = func
    
