import pygame
import math
from functools import cmp_to_key
from object import object

class textBox(object):
    whiteBar = False
    screenColor = (0, 0, 0)
    rectColor = (255, 255, 255)
    isMoving = False
    propertyToColor = {
        'NORMAL' : ((255,255,255),(0, 0, 0)),   # 입력 중인 텍스트
        'BLANK' : None,                         # 공백
        'ACTIVE' : ((0, 255, 255),(0, 0, 0)),
    }

    def __init__(self, p, s, f, d, ml=15) -> None:
        super().__init__(p, s)
        self.font = f
        self.maxLength = ml  # 입력창의 길이
        self.table = [('궳', 'BLANK')] * ml # 입력창의 문자를 모은 리스트. 개별 원소는 ('문자', '속성')의 꼴임.
        self.fontSize = self.font.size('가')
        self.skillDictionary = d

    '''Length 관련 메서드'''

    def getBlankLen(self):  # Str 입력 시 사용 가능한 여유 공간을 반환함
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

    '''Str 관련 메서드'''

    def setStr(self, s):
        self.delStrFromRight(self.getMaxLength())
        self.addStr(s)

    def getStr(self):
        s = ''
        for (text, prop) in self.table:
            if prop != 'BLANK':
                s += text
        return s

    def getLen(self):
        return len(self.getStr())

    def addStr(self, s, propNew = 'NORMAL'):
        addCnt = 0
        for i in range(self.getMaxLength()):
            (text, prop) = self.table[i]
            if prop == 'BLANK' and addCnt < len(s):
                self.table[i] = (s[addCnt], propNew)
                addCnt += 1

    def delStrFromLeft(self, k):  # 가장 왼쪽 k개의 문자를 제거하고 제거한 문자열 반환함
        removeCnt = 0
        removedText = []
        for i in range(self.getMaxLength()):
            (text, prop) = self.table[i]

            if prop == 'NORMAL' and removeCnt < k:
                removedText += self.table[i]
                self.table[i] = ('궳', 'BLANK')
                removeCnt += 1

        return removedText

    def delStrFromRight(self, k):  # 가장 오른쪽 k개의 문자를 제거하고 제거한 문자열 반환함
        removeCnt = 0
        removedText = []
        for i in range(self.getMaxLength()-1, -1, -1):
            (text, prop) = self.table[i]

            if prop == 'NORMAL' and removeCnt < k:
                removedText += self.table[i]
                self.table[i] = ('궳', 'BLANK')
                removeCnt += 1

        return removedText

    '''색 관련 메서드'''
    def getColor(self, property):
        return self.propertyToColor[property]

    '''Dictionary 관련 메서드'''
    def isValid(self):
        return self.getStr() in self.skillDictionary
    
    def addSkill(self):
        pass

    def delSkill(self):
        pass

    '''
    테이블 정렬 메서드
    def sortTable(self):
        def propertyOrder(x1, x2):
            prop1 = x1[1]
            prop2 = x2[1]
            propertyOrder = {'NORMAL' : -1, 'ACTVIE' : -1, 'BLANK' : 0}
            return propertyOrder[prop1] - propertyOrder[prop2]       
        self.table = sorted(self.table, key = cmp_to_key(propertyOrder))
    '''

    '''출력 메서드'''
    def draw(self):
        (x, y) = self._pos
        (_x, _y) = self._pos_init
        x += self.fontSize[0] * (self.getMaxLength() - self.getLen()) / 2
        cnt = 0
        for i in range(self.maxLength):
            (text, property) = self.table[i]
            if property == 'BLANK':
                pass
            else:
                if self.isValid():
                    (textColor, backgroundColor) = self.getColor('ACTIVE')
                else:
                    (textColor, backgroundColor) = self.getColor(property)
                toDraw = self.font.render(text, True, textColor, backgroundColor)
                if self.isMoving:
                    dy = abs(y - _y)
                    wiggle = self.skillDictionary[self.getStr()]['WIGGLE']
                    frequency = self.skillDictionary[self.getStr()]['FREQUENCY']
                    dx_wiggle = wiggle * 1.5 * math.sin(dy/frequency * 2 * math.pi + cnt**2) * (dy/300)**0.25 * (1 - dy/300)
                    dy_wiggle = wiggle * math.sin(dy/frequency * 2 * math.pi + cnt**2) * (dy/300)**0.25 * (1 - dy/300)
                    self.getScreen().blit(toDraw, (x + cnt * self.fontSize[0] + dx_wiggle, y + dy_wiggle))
                else:
                    self.getScreen().blit(toDraw, (x + cnt * self.fontSize[0], y))
                cnt += 1

        if self.isMoving:
            pass
        else:
            pygame.draw.rect(self.getScreen(), self.rectColor, [self._pos[0]-10, self._pos[1]-4, self.fontSize[0]*self.getMaxLength()+20, self.fontSize[1]+8], 4)