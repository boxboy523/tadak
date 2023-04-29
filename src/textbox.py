import pygame
from functools import cmp_to_key
import object

class textBox(object):
    whiteBar = False
    screenColor = (0, 0, 0)
    rectColor = (255, 255, 255)
    isValid = False
    isMoving = False
    propertyToColor = {
        'NORMAL' : ((255,255,255),(0, 0, 0)),   # 입력 중인 텍스트
        'PARRIED' : ((255, 200, 0),(0, 0, 0)),  # 패리된 텍스트
        'BLANK' : None,                         # 공백
        'ACTIVE' : ((0, 255, 255),(0, 0, 0)), 
        'STUNNED' : ((0,0,0),(255, 255, 0))     # 이미 스턴되어 오른쪽에 정렬된 텍스트
    }

    def __init__(self, p, s, f, ml=15) -> None:
        super().__init__(p, s)
        self.font = f
        self.maxLength = ml  # 입력창의 길이
        self.table = [('궳', 'BLANK')] * ml # 입력창의 문자를 모은 리스트. 개별 원소는 ('문자', '속성')의 꼴임.
        self.fontSize = self.font.size('가')

    '''Length 관련 메서드'''

    def getBlankLen(self):  # MainStr 입력 시 사용 가능한 여유 공간을 반환함
        numBlank = 0
        for (text, property) in self.table:
            if property == 'BLANK':
                numBlank += 1
        return numBlank

    def getSpareLen(self):  # StunStr 입력 시 사용 가능한 여유 공간을 반환함
        numSpare = 0
        for (text, property) in self.table:
            if property == 'BLANK' or property == 'NORMAL':
                numSpare += 1
        return numSpare

    def setMaxLength(self, i):
        if i < self.maxLength:
            self.table = self.table[0:i]
        elif i > self.maxLength:
            self.table += [('궳', 'BLANK')] * (i - self.maxLength)
        self.sortTable()
        self.maxLength = i

    def getMaxLength(self):
        return self.maxLength

    '''MainStr 관련 메서드'''

    def setMainStr(self, s):
        self.subMainStrFromRight(self.getMaxLength(), True)
        self.addMainStr(s)

    def getMainStr(self):
        s = ''
        for (text, property) in self.table:
            if property == 'NORMAL' or property == 'PARRIED':
                s += text
        return s

    def getMainLen(self):
        return len(self.getMainStr())
    
    def getLastText(self):
        if self.getMainLen() == 0: return None
        return self.table[self.getMainLen() - 1][0]

    def addMainStr(self, s, inputProperty = 'NORMAL'):
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(s):
                self.table[currIdx] = (s[numAdd], inputProperty)
                numAdd += 1
        self.sortTable()

    def subMainStrFromLeft(self, i, subPreStun = False):  # 가장 왼쪽 i개의 문자를 제거함
        toRemove = i
        textRemoved = []
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'PARRIED' and not subPreStun:
                break
            elif (property == 'NORMAL' or property == 'PARRIED') and toRemove > 0:
                textRemoved += self.table[currIdx]
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()
        return textRemoved

    def subMainStrFromRight(self, i, subPreStun = False):  # 가장 오른쪽 i개의 문자를 제거함
        toRemove = i
        textRemoved = []
        for curr in range(self.getMaxLength()):
            currIdx = (self.getMaxLength() - 1) - curr
            (text, property) = self.table[currIdx]
            if property == 'PARRIED' and not subPreStun:
                break
            elif (property == 'NORMAL' or property == 'PARRIED') and toRemove > 0:
                textRemoved += self.table[currIdx]
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()
        return textRemoved
    
    '''Parry 관련 메서드'''
    def parry(self):
        self.subMainStrFromRight(1)

    def isParried(self):
        return self.table[self.getMainLen() - 1][1] == 'PARRIED'

    def getParried(self):
        L = self.subMainStrFromRight(1)
        self.addMainStr(L[0][0], 'PARRIED')

    def parryNum(self):
        cnt = 0
        for (text, property) in self.table:
            if property == 'PARRIED':
                cnt += 1
        return cnt
    
    def getStunned(self):
        s = self.getMainStr()
        self.setMainStr('')
        self.addStunStr(s)

    '''StunStr 관련 메서드'''

    def setStunStr(self, s):
        self.subStunStrFromRight(self.getMaxLength())
        self.addStunStr(s)

    def getStunStr(self):
        s = ''
        for (text, property) in self.table:
            if property == 'STUNNED':
                s += text
        return s

    def getStunLen(self):
        return len(self.getStunStr())

    def addStunStr(self, s):
        stunText = self.getStunStr() + s
        self.subMainStrFromRight(len(s) - self.getBlankLen())
        self.subStunStrFromLeft(self.getMaxLength())
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUNNED')
                numAdd += 1
        self.sortTable()       
        '''
        stunText = self.getStunStr() + s
        self.subStunStrFromLeft(self.getMaxLength())
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUNNED')
                numAdd += 1
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if (property == 'NORMAL' or property == 'PARRIED') and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUNNED')
                numAdd += 1
        self.sortTable()
        '''

    def subStunStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        toRemove = i
        textRemoved = []
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'STUNNED' and toRemove > 0:
                textRemoved += self.table[currIdx]
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()
        return textRemoved

    def subStunStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        toRemove = i
        textRemoved = []
        for curr in range(self.getMaxLength()):
            currIdx = (self.getMaxLength() - 1) - curr
            (text, property) = self.table[currIdx]
            if property == 'STUNNED' and toRemove > 0:
                textRemoved += self.table[currIdx]
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()
        return textRemoved

    '''테이블 정렬 메서드'''
    def sortTable(self):
        def propertyOrder(x1, x2):
            prop1 = x1[1]
            prop2 = x2[1]
            propertyOrder = {'NORMAL' : -1, 'PARRIED' : -1, 'BLANK' : 0, 'STUNNED' : 1}
            return propertyOrder[prop1] - propertyOrder[prop2]
        
        self.table = sorted(self.table, key = cmp_to_key(propertyOrder))

    '''색 관련 메서드'''

    def getColor(self, property):
        return self.propertyToColor[property]
    
    '''출력 메서드'''

    def draw(self):
        (x, y) = self._pos
        x += self.fontSize[0] * (self.getMaxLength() - self.getMainLen()) / 2
        for (text, property) in self.table:
            if property == 'BLANK':
                pass
            else:
                if self.isValid:
                    (textColor, backgroundColor) = self.getColor('ACTIVE')
                else:
                    (textColor, backgroundColor) = self.getColor(property)
                toDraw = self.font.render(text, True, textColor, backgroundColor)
                self.getScreen().blit(toDraw, (x, y))
            x += self.fontSize[0]
        if self.isMoving:
            pygame.draw.rect(self.getScreen(), self.screenColor, [self._pos[0]-4, self._pos[1]-4, self.fontSize[0]*self.getMaxLength()+8, self.fontSize[1]+8], 4)
        else:
            pygame.draw.rect(self.getScreen(), self.rectColor, [self._pos[0]-4, self._pos[1]-4, self.fontSize[0]*self.getMaxLength()+8, self.fontSize[1]+8], 4)
        '''
        stunText = self.font.render(self.stunStr, True, self.stunColor, self.stunself.getScreen())
        if isValid: mainText = self.font.render(self.mainStr, True, self.actionColor)
        else: mainText = self.font.render(self.mainStr, True, self.mainColor)
    
        self.getScreen().blit(stunText, (self._pos[0]+(self.getBlankLen()+len(self.mainStr))*self.fontSize[0],self._pos[1]))
        self.getScreen().blit(mainText, self._pos)

        pygame.draw.rect(self.getScreen(), self.rectColor, [self._pos[0]-4, self._pos[1]-4, self.fontSize[0]*self.maxLength+8, self.fontSize[1]+8], 4)
        '''
