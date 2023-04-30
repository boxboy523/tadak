import pygame
from functools import cmp_to_key
from object import object

class textBox(object):
    whiteBar = False
    screenColor = (0, 0, 0)
    rectColor = (255, 255, 255)
    isValid = False
    isMoving = False
    propertyToColor = {
        'NORMAL' : ((255,255,255),(0, 0, 0)),   # 입력 중인 텍스트
        'BLANK' : None,                         # 공백
        'ACTIVE' : ((0, 255, 255),(0, 0, 0)),
    }

    def __init__(self, p, s, f, ml=15) -> None:
        super().__init__(p, s)
        self.font = f
        self.maxLength = ml  # 입력창의 길이
        self.table = [('궳', 'BLANK')] * ml # 입력창의 문자를 모은 리스트. 개별 원소는 ('문자', '속성')의 꼴임.
        self.fontSize = self.font.size('가')

    '''Length 관련 메서드'''

    def getBlankLen(self):  # MainStr 입력 시 사용 가능한 여유 공간을 반환함
        cnt = 0
        for (text, property) in self.table:
            if property == 'BLANK':
                cnt += 1
        return cnt

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
        self.subMainStrFromRight(self.getMaxLength())
        self.addMainStr(s)

    def getMainStr(self):
        s = ''
        for (text, property) in self.table:
            if property == 'NORMAL':
                s += text
        return s

    def getMainLen(self):
        return len(self.getMainStr())
    
    def getLastText(self):
        if self.getMainLen() == 0: return None
        return self.table[self.getMainLen() - 1][0]

    def addMainStr(self, s):
        addCnt = 0
        for i in range(self.getMaxLength()):
            (text, prop) = self.table[i]
            if prop == 'BLANK' and addCnt < len(s):
                self.table[i] = (s[addCnt], 'NORMAL')
                addCnt += 1
        self.sortTable()

    def subMainStrFromLeft(self, k):  # 가장 왼쪽 k개의 문자를 제거하고 제거한 문자열 반환함
        removeCnt = 0
        removedText = []
        for i in range(self.getMaxLength()):
            (text, prop) = self.table[i]

            if prop == 'NORMAL' and removeCnt < k:
                removedText += self.table[i]
                self.table[i] = ('궳', 'BLANK')
                removeCnt += 1

        return removedText

    def subMainStrFromRight(self, k):  # 가장 오른쪽 k개의 문자를 제거하고 제거한 문자열 반환함
        removeCnt = 0
        removedText = []
        for i in range(self.getMaxLength()-1, -1, -1):
            (text, property) = self.table[i]

            if property == 'NORMAL' and removeCnt < k:
                removedText += self.table[i]
                self.table[i] = ('궳', 'BLANK')
                removeCnt += 1

        return removedText

    '''색 관련 메서드'''
    def getColor(self, property):
        return self.propertyToColor[property]
    
    '''테이블 정렬 메서드'''
    def sortTable(self):
        def propertyOrder(x1, x2):
            prop1 = x1[1]
            prop2 = x2[1]
            propertyOrder = {'NORMAL' : -1, 'ACTVIE' : -1, 'BLANK' : 0}
            return propertyOrder[prop1] - propertyOrder[prop2]
        
        self.table = sorted(self.table, key = cmp_to_key(propertyOrder))


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