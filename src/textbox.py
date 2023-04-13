import pygame
from functools import cmp_to_key

class textBox:
    whiteBar = False
    screenColor = (0, 0, 0)
    rectColor = (255, 255, 255)
    propertyToColor = {'MAIN' : ((255,255,255),(0, 0, 0)), 'PRE_STUN' : ((150, 150, 0),(0, 0, 0)), 'BLANK' : None, 'STUN' : ((0,0,0),(255, 255, 0))}
    '''
        BLANK : 공백
        MAIN : 입력 중인 텍스트
        PRE_STUN : 입력 도중 스턴된 텍스트
        STUN : 이미 스턴되어 오른쪽에 정렬된 텍스트
    '''
    def __init__(self, f, ml=15) -> None:
        self.font = f
        self.maxLength = ml  # 입력창의 길이
        self.table = [('궳', 'BLANK')] * ml # 입력창의 문자를 모은 리스트. 개별 원소는 ('문자', '속성')의 꼴임.
        self.fontSize = self.font.size("가")

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
            if property == 'BLANK' or property == 'MAIN':
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
            if property == 'MAIN' or property == 'PRE_STUN':
                s += text
        return s

    def getMainLen(self):
        return len(self.getMainStr())

    def addMainStr(self, s):
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(s):
                self.table[currIdx] = (s[numAdd], 'MAIN')
                numAdd += 1
        self.sortTable()

    def subMainStrFromLeft(self, i, subPreStun = False):  # 가장 왼쪽 i개의 문자를 제거함
        toRemove = i
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'PRE_STUN' and not subPreStun:
                break
            elif property == 'MAIN' and toRemove > 0:
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()

    def subMainStrFromRight(self, i, subPreStun = False):  # 가장 오른쪽 i개의 문자를 제거함
        toRemove = i
        for curr in range(self.getMaxLength()):
            currIdx = (self.getMaxLength() - 1) - curr
            (text, property) = self.table[currIdx]
            if property == 'PRE_STUN' and not subPreStun:
                break
            elif property == 'MAIN' and toRemove > 0:
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()

    '''StunStr 관련 메서드'''

    def setStunStr(self, s):
        self.subStunStrFromRight(self.getMaxLength())
        self.addStunStr(s)

    def getStunStr(self):
        s = ''
        for (text, property) in self.table:
            if property == 'STUN':
                s += text
        return s

    def getStunLen(self):
        return len(self.getStunStr())

    def addStunStr(self, s):
        stunText = self.getStunStr() + s
        self.subMainStrFromRight(len(stunText) - self.getBlankLen())
        self.subStunStrFromLeft(self.getMaxLength())
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUN')
                numAdd += 1
        self.sortTable()       
        '''
        stunText = self.getStunStr() + s
        self.subStunStrFromLeft(self.getMaxLength())
        numAdd = 0
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'BLANK' and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUN')
                numAdd += 1
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if (property == 'MAIN' or property == 'PRE_STUN') and numAdd < len(stunText):
                self.table[currIdx] = (stunText[numAdd], 'STUN')
                numAdd += 1
        self.sortTable()
        '''

    def subStunStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        toRemove = i
        for currIdx in range(self.getMaxLength()):
            (text, property) = self.table[currIdx]
            if property == 'STUN' and toRemove > 0:
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()

    def subStunStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        toRemove = i
        for curr in range(self.getMaxLength()):
            currIdx = (self.getMaxLength() - 1) - curr
            (text, property) = self.table[currIdx]
            if property == 'STUN' and toRemove > 0:
                self.table[currIdx] = ('궳', 'BLANK')
                toRemove -= 1
        self.sortTable()

    '''테이블 정렬 메서드'''
    def sortTable(self):
        def propertyOrder(x1, x2):
            prop1 = x1[1]
            prop2 = x2[1]
            propertyOrder = {'MAIN' : -1, 'PRE_STUN' : -1, 'BLANK' : 0, 'STUN' : 1}
            return propertyOrder[prop1] - propertyOrder[prop2]
        
        self.table = sorted(self.table, key = cmp_to_key(propertyOrder))

    '''색 관련 메서드'''

    def getColor(self, property):
        return self.propertyToColor[property]
    
    '''출력 메서드'''

    def drawBox(self, screen, pos, isValid):
        (x, y) = pos
        for (text, property) in self.table:
            if property == 'BLANK':
                pass
            else:
                (textColor, backgroundColor) = self.getColor(property)
                toDraw = self.font.render(text, True, textColor, backgroundColor)
                screen.blit(toDraw, (x, y))
            x += self.fontSize[0]
        pygame.draw.rect(screen, self.rectColor, [pos[0]-4, pos[1]-4, self.fontSize[0]*self.getMaxLength()+8, self.fontSize[1]+8], 4)

        '''
        stunText = self.font.render(self.stunStr, True, self.stunColor, self.stunScreen)
        if isValid: mainText = self.font.render(self.mainStr, True, self.actionColor)
        else: mainText = self.font.render(self.mainStr, True, self.mainColor)
    
        screen.blit(stunText, (pos[0]+(self.getBlankLen()+len(self.mainStr))*self.fontSize[0],pos[1]))
        screen.blit(mainText, pos)

        pygame.draw.rect(screen, self.rectColor, [pos[0]-4, pos[1]-4, self.fontSize[0]*self.maxLength+8, self.fontSize[1]+8], 4)
        '''
