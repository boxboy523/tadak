import pygame


class textBox:
    whiteBar = False

    def __init__(self, f, ml=15, c=(255, 255, 255), sc=(255, 255, 0), ac=(0, 255, 255), rc=(255, 255, 255)) -> None:
        self.font = f
        self.maxLength = ml  # 입력창의 길이

        self.mainStr = ''  # 입력 중인 텍스트
        self.stunStr = ''  # 스턴 텍스트

        self.mainColor = c  # 입력 텍스트 색깔 / 디폴트 : 하얀색
        self.stunColor = sc  # 스턴 텍스트 색깔 / 디폴트 : 노란색
        self.actionColor = ac  # 명령어 완성 시 텍스트 색깔 / 디폴트 : 하늘색
        self.rectColor = rc  # 입력창 박스 색깔 / 디폴트 : 하얀색

    def getRemainingLen(self):  # 입력창의 여유 공간을 반환함
        return self.maxLength - len(self.mainStr) - len(self.stunStr)

    def setMaxLength(self, i):
        self.maxLength = i

    # MainStr 관련 메서드

    def setMainStr(self, s):
        self.mainStr = s

    def getMainStr(self):
        return self.mainStr

    def getMainLen(self):
        return len(self.mainStr)

    def addMainStr(self, s):
        self.mainStr += s[0:self.getRemainingLen()]

    def subMainStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        self.mainStr = self.mainStr[min(i, len(self.mainStr)):]

    def subMainStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        self.mainStr = self.mainStr[:max(0, len(self.mainStr) - i)]

    # StunStr 관련 메서드

    def setStunStr(self, s):
        self.stunStr = s

    def getStunStr(self):
        return self.stunStr

    def addStunStr(self, s):
        self.stunStr += s[0:self.getRemainingLen()]

    def subStunStrFromLeft(self, i):  # 가장 왼쪽 i개의 문자를 제거함
        self.stunStr = self.mainStr[min(i, len(self.stunStr)):]

    def subStunStrFromRight(self, i):  # 가장 오른쪽 i개의 문자를 제거함
        self.stunStr = self.stunStr[:max(0, len(self.stunStr) - i)]

    # 색 관련 메서드

    def setColor(self, c):
        self.mainColor = c

    def drawBox(self, screen, pos):
        print(self.mainStr)
        allText = self.font.render(self.mainStr + ' ' * self.getRemainingLen() + self.stunStr, True, self.stunColor)
        mainText = self.font.render(self.mainStr, True, self.mainColor)
        pygame.draw.rect(screen, self.rectColor, [pos[0], pos[1], 710, self.font.size("a")[1]], 4)
        screen.blit(allText, pos)
        screen.blit(mainText, pos)
