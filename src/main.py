import pygame
import random
import time
import ime
import math

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
    my_height = 400
    enemy_height = 100
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TADAK")

    myFont = pygame.font.SysFont("Nanum Gothic", 30)
    myFontSmall = pygame.font.SysFont("Nanum Gothic", 20)
    myTextBox = textBox(myFont, ml=12)
    myTextLog = textLog(myFont, grad=True, ml=30, utd=False)
    mySkillList = ['화염구', '불덩이작렬', '패리', '대규모냉각' , '볼트', '체인라이트닝']
    mySkillCoolDownDictionary = {'화염구': 600, '불덩이작렬' : 2000, '패리' : 200, '대규모냉각' : 1000, '볼트' : 300, '체인라이트닝' : 500}
    mySkillDamageDictionary = {'화염구': 6, '불덩이작렬' : 20, '패리' : 0, '대규모냉각' : 8, '볼트' : 2, '체인라이트닝' : 12}
    myHp = 30

    enemyTextBox = textBox(myFont, ml=12)
    enemySkillList = ['전투강타', '돌진', '방패던지기', '이제간다아아아아앗']
    enemySkillCoolDownDictionary = {'전투강타' : 800, '돌진' : 300, '방패던지기' : 500, '이제간다아아아아앗' : 1200}
    enemySkillDamageDictionary = {'전투강타' : 4, '돌진' : 2, '방패던지기' : 5, '이제간다아아아아앗' : 9}
    enemyCurrIdx = -1
    enemySkillSet = False
    enemyHp = 100
    enemyStatus = dict()

    global_t = 0
    global_frame = 0
    backSpace_t = 0
    backSpaceOffset = 0
    enemyOffset = 0
    isMyDoing = False
    isEnemyDoing = False
    myLeftStunTime = 0
    enemyLeftStunTime = 0
    enemyLastInput_t = 0

    backSpaceThreshold = 100 # backSpaceLatency의 하한(ms)
    backSpaceLatencyInit = 150 # backSpaceLatency의 초기값(ms)
    backSpaceAcceleration = 5 # backSpaceLatency가 감소하는 양(ms)
    backSpaceLatency = backSpaceLatencyInit  # 글자 하나 지우는 데 드는 시간(ms)

    enemyTypeIntervalInit = 200 # 상대가 음소 하나를 입력하는 데 걸리는 시간(ms)
    enemyTypeInterval = enemyTypeIntervalInit
    enemyTypeVarience = 100

    justParryThreshold = 200
    lateParryThreshold = 400
    enemyParryInterval = 1750
    myParryInterval = 750
    myParryTextLifeTime = 0

    running = True
    isKor = True
    shiftPressed = False

    exceptChar = [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LALT,
                  pygame.K_RALT]  # 글자 아닌 키들 분류

    while running:

        '''글로벌 타임'''
        clock.tick(fps)
        # print(f"tick:{clock.tick(fps)}   fps:{clock.get_fps()}") # fps 체크
        if enemyLeftStunTime > 0:
            enemyOffset += 1000 / fps

        '''값 입력'''
        for event in pygame.event.get():
            if isMyDoing:
                break

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
        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and not isMyDoing:  # 백스페이스 누르는 동안 backSpace_t 증가
            if backSpace_t == 0:
                bsp = myIME.backSpace()
                myTextBox.subMainStrFromRight(1)
                if bsp is not None:
                    myTextBox.addMainStr(bsp)
            backSpace_t += 1000 / fps
        else:
            backSpace_t = 0  # 떼면 초기화
            backSpaceOffset = 0
            backSpaceLatency = backSpaceLatencyInit

        '''엔터'''
        if pygame.key.get_pressed()[pygame.K_RETURN] and not isMyDoing:
            myIME.resetState()  # 엔터 후 IME()를 리셋해야 한다.
            if myTextBox.getMainStr() != '':
                '''행동 성공 시'''
                if myTextBox.getMainStr() in mySkillList:
                    myTextLog.addLine(myTextBox.getMainStr())
                    myDoingInterval = mySkillCoolDownDictionary[myTextBox.getMainStr()]
                    myLeftStunTime += myDoingInterval
                    isMyDoing = True
                else:
                    myTextBox.setMainStr('')

        '''쉬프트'''
        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT] and not isMyDoing:            shiftPressed = True

        '''지우기 실행'''
        if myTextBox.getMainStr() != '':
            if backSpace_t - backSpaceOffset >= backSpaceLatency:
                myTextBox.subMainStrFromRight(1)
                backSpaceOffset += backSpaceLatency
                backSpaceLatency = max(backSpaceThreshold, backSpaceLatency - backSpaceAcceleration)

        '''내 행동 완료 체크'''
        if myLeftStunTime <= 0 and isMyDoing:
            isMyDoing = False
            enemyHp -= mySkillDamageDictionary[myTextBox.getMainStr()]

            if myTextBox.getMainStr() == '패리':
                if 0 < global_t - enemyLastInput_t < justParryThreshold and isEnemyDoing:
                    isEnemyDoing = False
                    enemyTextBox.setMainStr('')
                    enemyLeftStunTime = enemyParryInterval
                    myLeftStunTime = myParryInterval
                    myParryTextLifeTime = myParryInterval
                elif 0 < global_t - enemyLastInput_t < lateParryThreshold and isEnemyDoing:
                    isEnemyDoing = False
                    myHp -= enemySkillDamageDictionary[enemyTextBox.getMainStr()] // 2
                    enemyTextBox.setMainStr('')
                    myLeftStunTime = myParryInterval

            if myTextBox.getMainStr() == '화염구':
                if not '화상' in enemyStatus:
                    enemyStatus['화상'] = 0
                if enemyStatus['화상'] < 2:
                    enemyStatus['화상'] += 1

            if myTextBox.getMainStr() == '불덩이작렬':
                if not '화상' in enemyStatus:
                    enemyStatus['화상'] = 0
                if enemyStatus['화상'] < 2:
                    enemyStatus['화상'] += 1
                enemyLeftStunTime += 300
                
            if myTextBox.getMainStr() == '대규모냉각':
                if not '동상' in enemyStatus:
                    enemyStatus['동상'] = 0
                enemyStatus['동상'] += 1

            if myTextBox.getMainStr() == '볼트':
                if not '감전' in enemyStatus:
                    enemyStatus['감전'] = 0
                enemyStatus['감전'] += 1

            if myTextBox.getMainStr() == '체인라이트닝':
                if not '감전' in enemyStatus:
                    enemyStatus['감전'] = 0
                enemyStatus['감전'] += 3
            
            myTextBox.setMainStr('')
                
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

        '''적 행동 수행 체크'''
        if enemyCurrIdx == len(enemyLetter) and global_t - enemyOffset >= enemyTypeInterval / 3:
            enemyLastInput_t = global_t
            '''적 행동 성공시'''
            if enemyTextBox.getMainStr() in enemySkillList:
                enemyDoingInterval = enemySkillCoolDownDictionary[enemyTextBox.getMainStr()]
                enemyLeftStunTime += enemyDoingInterval
                isEnemyDoing = True
            enemyOffset += enemyTypeInterval + random.randrange(-1 * enemyTypeVarience, enemyTypeVarience + 1)
            enemyIME.resetState()
            enemySkillSet = False

        '''적 타이핑 수행'''
        if global_t - enemyOffset >= enemyTypeInterval:
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

        '''적 행동 완료 체크'''
        if enemyLeftStunTime <= 0 and isEnemyDoing:
            isEnemyDoing = False
            if enemyTextBox.getMainStr() in enemySkillList:
                myHp -= enemySkillDamageDictionary[enemyTextBox.getMainStr()]
            enemyTextBox.setMainStr('')

        '''상태이상'''
        if '화상' in enemyStatus :
            enemyHp -= 0.8 * enemyStatus['화상'] / fps
        if '감전' in enemyStatus:
            if enemyStatus['감전'] >= 4:
                del enemyStatus['감전']
                enemyLeftStunTime += 1000
                enemyTextBox.setMainStr('')
                enemySkillSet = False
        if '동상' in enemyStatus:
            enemyTypeInterval = (2 - (0.8)**enemyStatus['동상']) * enemyTypeIntervalInit 

        '''화면 출력'''
        screen.fill(pygame.Color("black"))

        '''HP 출력'''
        myHpText = myFont.render("HP : " + str(math.ceil(myHp)), True, (255, 255, 255))
        screen.blit(myHpText, (100, my_height))
        enemyHpText = myFont.render("HP : " + str(math.ceil(enemyHp)), True, (255, 255, 255))
        screen.blit(enemyHpText, (100, enemy_height))

        '''상태이상 출력'''
        enemyStatusText = myFont.render(str(enemyStatus), True, (255, 255, 255))
        screen.blit(enemyStatusText, (300, 50))

        '''가능한 행동 출력'''
        s = ''
        for atk in mySkillList:
            s += (atk + ' / ')
        atkText = myFontSmall.render(s[:len(s)-3], True, (0, 255, 255))
        screen.blit(atkText, (400, 550))

        '''로그 및 입력창 출력'''
        myTextLog.draw(screen, (800, 400))
        if isMyDoing:
            myTextBox.drawBox(screen, ((screen_width - myTextBox.fontSize[0] * myTextBox.getMaxLength()) / 2, my_height * (myLeftStunTime / myDoingInterval)**4 + enemy_height * (1 - (myLeftStunTime / myDoingInterval)**4)), myTextBox.getMainStr() in mySkillList, myLeftStunTime > 0)
        else:
            myTextBox.drawBox(screen, ((screen_width - myTextBox.fontSize[0] * myTextBox.getMaxLength()) / 2, my_height), myTextBox.getMainStr() in mySkillList, myLeftStunTime > 0)
        
        if isEnemyDoing:
            enemyTextBox.drawBox(screen, ((screen_width - enemyTextBox.fontSize[0] * enemyTextBox.getMaxLength()) / 2, enemy_height * (enemyLeftStunTime / enemyDoingInterval)**4 + my_height * (1 - (enemyLeftStunTime / enemyDoingInterval)**4)), enemyTextBox.getMainStr() in enemySkillList, enemyLeftStunTime > 0)
        else:
            enemyTextBox.drawBox(screen, ((screen_width - enemyTextBox.fontSize[0] * enemyTextBox.getMaxLength()) / 2, enemy_height), enemyTextBox.getMainStr() in enemySkillList, enemyLeftStunTime > 0)
        
        '''패리 출력'''
        if myParryTextLifeTime > 0: 
            parryText = myFont.render("패리!!", True, (255, 255, 0))
            screen.blit(parryText, (450, 250))

        '''승패 판정 출력'''
        if myHp <= 0:
            gameOverText = myFont.render("죽었다...", True, (255, 255, 255))
            screen.blit(gameOverText, (350, 250))
            pygame.display.update()
            time.sleep(2)
            break
        elif enemyHp <= 0:
            gameOverText = myFont.render("적을 쓰러뜨렸다!", True, (255, 255, 255))
            screen.blit(gameOverText, (350, 250))
            pygame.display.update()
            time.sleep(2)
            break

        '''시간 변경'''

        global_t += 1000 / fps
        global_frame += 1
        if myLeftStunTime > 0: myLeftStunTime -= 1000 / fps
        if enemyLeftStunTime > 0: enemyLeftStunTime -= 1000 / fps
        if myParryTextLifeTime > 0: myParryTextLifeTime -= 1000 / fps

        pygame.display.update()


if __name__ == "__main__":
    game()
