import pygame
import random
import time
import ime

from textbox import textBox
from textlog import textLog
from ime import IME

pygame.init()


def game():
    clock = pygame.time.Clock()
    fps = 60

    myIME = IME()
    enemyIME = IME()

    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TADAK")

    myFont = pygame.font.SysFont("Nanum Gothic", 30)
    myTextBox = textBox(myFont, ml=20)
    myTextLog = textLog(myFont, grad=True, ml=30, utd=False)
    mySkillList = ['토네이도', '사격', '파지직']
    myLeftBomb = 1

    enemyTextBox = textBox(myFont, ml=30)
    enemySkillList = ['지진']
    enemyCurrIdx = -1
    enemyCurrSkill = ''
    enemySkillSet = False

    myParrySuccess = False
    enemyParrySuccess = False
    parryText = ''
    myParryThreshold = 150 * (fps / 1000)  # 내 Parry가 인정되는 시간의 상한(ms)
    enemyParryThreshold = 150 * (fps / 1000)  # 상대의 Parry가 인정되는 시간의 상한(ms)

    global_t = 0
    backSpace_t = 0
    myLastInput_t = 0
    enemyLastInput_t = 0
    backSpaceOffset = 0
    enemyOffset = 0

    backSpaceThreshold = 60 * (fps / 1000)  # backSpaceLatency의 하한(ms)
    backSpaceLatencyInit = 80 * (fps / 1000)  # backSpaceLatency의 초기값(ms)
    backSpaceAcceleration = 5 * (fps / 1000)  # backSpaceLatency가 감소하는 양(ms)
    backSpaceLatency = backSpaceLatencyInit  # 글자 하나 지우는 데 드는 시간(ms)

    enemyTypeInterval = 200 * (fps / 1000)  # 상대가 음소 하나를 입력하는 데 걸리는 시간(ms)
    enemyTypeVarience = 50 * (fps / 1000) 

    running = True
    isKor = True
    shiftPressed = False

    exceptChar = [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LALT,
                  pygame.K_RALT]  # 글자 아닌 키들 분류

    while running:
        '''글로벌 타임'''
        clock.tick(fps)
        # print(f"tick:{clock.tick(fps)}   fps:{clock.get_fps()}") # fps 체크
        '''값 입력'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_LALT, pygame.K_RALT]:
                    isKor = not isKor

                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    shiftPressed = True

                if event.key not in exceptChar:
                    myLastInput_t = global_t
                    try:
                        c = chr(event.key)
                        if shiftPressed and (97 <= ord(c) <= 122):
                            c = c.upper()
                        keyTuple = myIME.getKey(c, isKor)
                        if keyTuple[1]:
                            try:
                                myTextBox.addMainStr(keyTuple[0])
                            except:
                                pass
                        else:
                            try:
                                property = myTextBox.subMainStrFromRight(1, True)[1]
                                myTextBox.addMainStr(keyTuple[0], property)
                            except:
                                pass

                        if len(keyTuple) == 4:
                            if keyTuple[3]:
                                try:
                                    myTextBox.addMainStr(keyTuple[2])
                                except:
                                    pass
                            else:
                                try:
                                    property = myTextBox.subMainStrFromRight(1, True)[1]
                                    myTextBox.addMainStr(keyTuple[2], property)
                                except:
                                    pass
                    except:
                        pass

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    shiftPressed = False
        '''백스페이스'''
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # 백스페이스 누르는 동안 backSpace_t 증가
            if backSpace_t == 0:
                bsp = myIME.backSpace()
                myTextBox.subMainStrFromRight(1)
                if bsp is not None:
                    myTextBox.addMainStr(bsp)
            backSpace_t += 1
        else:
            backSpace_t = 0  # 떼면 초기화
            backSpaceOffset = 0
            backSpaceLatency = backSpaceLatencyInit
        '''엔터'''
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            myIME.resetState()  # 엔터 후 IME()를 리셋해야 한다.
            if myTextBox.getMainStr() != '':
                '''행동 성공 시'''
                if myTextBox.getMainStr() in mySkillList:
                    myTextLog.addLine(myTextBox.getMainStr())
                    enemyTextBox.addStunStr(myTextBox.getMainStr())
                if myTextBox.getMainStr() == '폭탄':
                    myTextLog.addLine(myTextBox.getMainStr())
                    if myLeftBomb > 0:
                        myLeftBomb -= 1
                        myTextBox.setStunStr('')
                    else:
                        pass  # 폭탄이 부족하다! 메세지
                myTextBox.setMainStr('')
        '''쉬프트'''
        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
            shiftPressed = True
        '''백스페이스 적용'''
        if myTextBox.getMainStr() != '':
            if backSpace_t - backSpaceOffset >= backSpaceLatency:
                myTextBox.subMainStrFromRight(1)
                backSpaceOffset += backSpaceLatency
                backSpaceLatency = max(backSpaceThreshold, backSpaceLatency - backSpaceAcceleration)
                
        '''적 행동 재설정'''
        if not enemySkillSet:
            enemyCurrSkill = enemySkillList[random.randint(
                0, len(enemySkillList) - 1)]
            enemyCurrIdx = 0
            enemyLetter = ''
            for i in range(len(enemyCurrSkill)):
                (x, y, z) = ime.get_jm(enemyCurrSkill[i])
                if z == ' ':
                    enemyLetter += x + y
                else:
                    enemyLetter += x + y + z
            enemySkillSet = True

        '''적 행동 완료 체크'''
        if enemyCurrIdx == len(enemyLetter) and global_t - enemyOffset >= enemyTypeInterval:
            if enemyTextBox.getMainStr() in enemySkillList and enemyTextBox.parryMinusNormal() < 0:
                myTextBox.addStunStr(enemyTextBox.getMainStr())
            enemyOffset += enemyTypeInterval + random.randrange(-1 * enemyTypeVarience, enemyTypeVarience + 1)
            enemyTextBox.setMainStr('')
            enemyIME.resetState()
            enemySkillSet = False

        '''적 타이핑 수행'''
        if global_t - enemyOffset >= enemyTypeInterval:
            enemyLastInput_t = global_t
            c = enemyLetter[enemyCurrIdx]
            keyTuple = enemyIME.getKey(c, True)
            if keyTuple[1]:
                try:
                    enemyTextBox.addMainStr(keyTuple[0])
                except:
                   pass
            else:
                try:
                    property = enemyTextBox.subMainStrFromRight(1, True)[1]
                    enemyTextBox.addMainStr(keyTuple[0], property)
                except:
                    pass

            if len(keyTuple) == 4:
                if keyTuple[3]:
                    try:
                        enemyTextBox.addMainStr(keyTuple[2])
                    except:
                        pass
                else:
                    try:
                        property = enemyTextBox.subMainStrFromRight(1, True)[1]
                        enemyTextBox.addMainStr(keyTuple[2], property)
                    except:
                        pass
            enemyOffset += enemyTypeInterval
            enemyCurrIdx += 1

        '''패리'''
        myParrySuccess = False
        enemyParrySuccess = False
        if myTextBox.getLastText() == enemyTextBox.getLastText() and myTextBox.getLastText() != None:  # 현재 뒷 글자가 겹치면 & 공백이 아니면
            if not ime.is_jaum(myTextBox.getLastText()) and not myTextBox.isParried() and not enemyTextBox.isParried():  # 겹치는 글자가 단자음이 아니라면
                if myLastInput_t >= enemyLastInput_t and myLastInput_t - enemyLastInput_t <= myParryThreshold:
                    myParrySuccess = True
                    myTextBox.parry()
                    myIME.resetState()
                    enemyTextBox.getParried()
                elif myLastInput_t < enemyLastInput_t and enemyLastInput_t - myLastInput_t <= enemyParryThreshold:
                    enemyParrySuccess = True
                    enemyTextBox.parry()
                    enemyIME.resetState()
                    myTextBox.getParried()

        global_t += 1

        '''화면 출력'''
        screen.fill(pygame.Color("black"))
        '''현재 상태'''
        bombText = myFont.render(
            "남은 폭탄 수 : " + str(myLeftBomb), True, (255, 255, 255))
        screen.blit(bombText, (100, 500))
        '''가능한 행동 출력'''
        s = ''
        for atk in mySkillList:
            s += (atk + ' / ')
        atkText = myFont.render(s[:len(s)-3], True, (0, 255, 255))
        screen.blit(atkText, (400, 500))
        '''입력창'''
        myTextLog.draw(screen, (100, 400))
        myTextBox.drawBox(screen, (100, 400),
                          myTextBox.getMainStr() in mySkillList)
        enemyTextBox.drawBox(screen, (100, 100),
                             enemyTextBox.getMainStr() in enemySkillList)
        '''패리'''
        if myParrySuccess: 
            parryText = myFont.render("PARRY!", True, (255, 255, 255))
            screen.blit(parryText, (350, 250))
        if enemyParrySuccess: 
            parryText = myFont.render("PARRIED...", True, (255, 255, 255))
            screen.blit(parryText, (350, 250))
        '''승패 판정'''
        if myTextBox.getStunLen() == myTextBox.getMaxLength():
            gameOverText = myFont.render("죽었다...", True, (255, 255, 255))
            screen.blit(gameOverText, (350, 250))
            pygame.display.update()
            time.sleep(2)
            break

        if enemyTextBox.getStunLen() == enemyTextBox.maxLength:
            gameOverText = myFont.render("적을 쓰러뜨렸다!", True, (255, 255, 255))
            screen.blit(gameOverText, (350, 250))
            pygame.display.update()
            time.sleep(2)
            break

        pygame.display.update()


if __name__ == "__main__":
    game()
