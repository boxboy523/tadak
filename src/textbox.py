import pygame


class textBox:
    whiteBar = False
    screenColor = (0, 0, 0)

    def __init__(self, f, ml=15, c=(255, 255, 255), sc=(0, 0, 0),ss=(255,255,0), ac=(0, 255, 255), rc=(255, 255, 255)) -> None:
        self.font = f
        self.maxLength = ml  # 입력창의 길이

        self.mainStr = ''  # 입력 중인 텍스트
        self.stunStr = ''  # 스턴 텍스트

        self.mainColor = c  # 입력 텍스트 색깔 / 디폴트 : 하얀색
        self.stunColor = sc  # 스턴 텍스트 색깔 / 디폴트 : 노란색
        self.stunScreen = ss
        self.actionColor = ac  # 명령어 완성 시 텍스트 색깔 / 디폴트 : 하늘색
        self.rectColor = rc  # 입력창 박스 색깔 / 디폴트 : 하얀색
        self.fontSize = self.font.size("가")

    '''Length 관련 메서드'''

    def getLeftLen(self):  # MainStr 입력 시 사용 가능한 여유 공간을 반환함
        return self.maxLength - len(self.mainStr) - len(self.stunStr)

    def getSpareLen(self):  # StunStr 입력 시 사용 가능한 여유 공간을 반환함
        return self.maxLength - len(self.stunStr)

    def setMaxLength(self, i):
        self.maxLength = i

    def getMaxLength(self):
        return self.maxLength

    '''MainStr 관련 메서드'''

    def setMainStr(self, s):
        self.mainStr = s

    def getMainStr(self):
        return self.mainStr

    def getMainLen(self):
        return len(self.mainStr)

    def addMainStr(self, s):
        self.mainStr += s[0:self.getLeftLen()]

    def subMainStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        self.mainStr = self.mainStr[min(i, len(self.mainStr)):]

    def subMainStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        self.mainStr = self.mainStr[:max(0, len(self.mainStr) - i)]

    '''StunStr 관련 메서드'''

    def setStunStr(self, s):
        self.stunStr = s

    def getStunStr(self):
        return self.stunStr

    def getStunLen(self):
        return len(self.stunStr)

    def addStunStr(self, s):
        self.stunStr += s[0:self.getSpareLen()]
        self.subMainStrFromRight(max(0, self.getMainLen() + self.getStunLen() - self.maxLength))

    def subStunStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        self.stunStr = self.mainStr[min(i, len(self.stunStr)):]

    def subStunStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        self.stunStr = self.stunStr[:max(0, len(self.stunStr) - i)]

    '''색 관련 메서드'''

    def setColor(self, c):
        self.mainColor = c

    
    '''출력 메서드'''


    def drawBox(self, screen, pos, isValid):
        stunText = self.font.render(self.stunStr, True, self.stunColor, self.stunScreen)
        if isValid: mainText = self.font.render(self.mainStr, True, self.actionColor)
        else: mainText = self.font.render(self.mainStr, True, self.mainColor)
        
        screen.blit(stunText, (pos[0]+(self.getLeftLen()+len(self.mainStr))*self.fontSize[0],pos[1]))
        screen.blit(mainText, pos)

        pygame.draw.rect(screen, self.rectColor, [pos[0]-4, pos[1]-4, self.fontSize[0]*self.maxLength+8, self.fontSize[1]+8], 4)
