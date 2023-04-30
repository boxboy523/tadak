import pygame
import random
import time
import ime
import math
import scene

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
    myScene = scene.scene(screen)

    myTextBox_initX = 300
    myTextBox_initY = 400
    enemyTextBox_initX = 300
    enemyTextBox_initY = 100

    myFont = pygame.font.Font("font/DungGeunMo.ttf", 30)
    myFontSmall = pygame.font.Font("font/DungGeunMo.ttf", 20)
    myTextBox = textBox((myTextBox_initX,myTextBox_initY), myScene, myFont, 12)
    myTextLog = textLog((800,myTextBox_initY), myScene, myFont, grad=True, ml=30, utd=False)
    mySkillList = ['화염구', '불덩이작렬', '패리', '대규모냉각' , '볼트', '체인라이트닝']
    mySkillCoolDownDictionary = {'화염구': 600, '불덩이작렬' : 2000, '패리' : 200, '대규모냉각' : 1000, '볼트' : 300, '체인라이트닝' : 500}
    mySkillDamageDictionary = {'화염구': 6, '불덩이작렬' : 20, '패리' : 0, '대규모냉각' : 8, '볼트' : 2, '체인라이트닝' : 12}
    myHp = 30

    enemyTextBox = textBox((myTextBox_initX,enemyTextBox_initY), myScene, myFont, 12)
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
    keyAvailable = True
    isMyMoving = False
    isEnemyMoving = False
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
    myParryTextOffset = -9999
    mySkillEffectOffset = -9999
    myParryTextLifeTime = myParryInterval
    mySkillEffectLifeTime = 500

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
            if not keyAvailable:
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
                                myTextBox.addStr(keyTuple[0])
                            except:
                                pass
                        else:
                            try:
                                myTextBox.subStrFromRight(1)
                                myTextBox.addStr(keyTuple[0])
                            except:
                                pass

                        if len(keyTuple) == 4:
                            if keyTuple[3]:
                                try:
                                    myTextBox.addStr(keyTuple[2])
                                except:
                                    pass
                            else:
                                try:
                                    myTextBox.subStrFromRight(1)
                                    myTextBox.addStr(keyTuple[2])
                                except:
                                    pass
                    except:
                        pass

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    shiftPressed = False

        '''백스페이스'''
        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and keyAvailable:  # 백스페이스 누르는 동안 backSpace_t 증가
            if backSpace_t == 0:
                bsp = myIME.backSpace()
                myTextBox.subStrFromRight(1)
                if bsp is not None:
                    myTextBox.addStr(bsp)
            backSpace_t += 1000 / fps
        else:
            backSpace_t = 0  # 떼면 초기화
            backSpaceOffset = 0
            backSpaceLatency = backSpaceLatencyInit

        '''엔터'''
        if pygame.key.get_pressed()[pygame.K_RETURN] and keyAvailable:
            myIME.resetState()  # 엔터 후 IME()를 리셋해야 한다.
            '''행동 성공 시'''
            if myTextBox.getStr() in mySkillList:
                myTextLog.addLine(myTextBox.getStr())
                myMovingInterval = mySkillCoolDownDictionary[myTextBox.getStr()]
                myLeftStunTime += myMovingInterval
                isMyMoving = True
                keyAvailable = False
            else:
                myTextBox.setStr('')

        '''쉬프트'''
        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT] and not keyAvailable:            shiftPressed = True

        '''지우기 실행'''
        if myTextBox.getStr() != '':
            if backSpace_t - backSpaceOffset >= backSpaceLatency:
                myTextBox.subStrFromRight(1)
                backSpaceOffset += backSpaceLatency
                backSpaceLatency = max(backSpaceThreshold, backSpaceLatency - backSpaceAcceleration)

        '''내 행동 완료 체크'''
        if myLeftStunTime <= 0 and isMyMoving:
            isMyMoving = False
            keyAvailable = True
            enemyHp -= mySkillDamageDictionary[myTextBox.getStr()]

            if myTextBox.getStr() == '패리':
                if 0 < global_t - enemyLastInput_t < justParryThreshold and isEnemyMoving:
                    isEnemyMoving = False
                    enemyTextBox.setStr('')
                    enemyLeftStunTime = enemyParryInterval
                    myLeftStunTime = myParryInterval
                    myParryTextOffset = global_t
                elif 0 < global_t - enemyLastInput_t < lateParryThreshold and isEnemyMoving:
                    isEnemyMoving = False
                    myHp -= enemySkillDamageDictionary[enemyTextBox.getStr()] // 2
                    enemyTextBox.setStr('')
                    myLeftStunTime = myParryInterval

            if myTextBox.getStr() == '화염구':
                if not '화상' in enemyStatus:
                    enemyStatus['화상'] = 0
                if enemyStatus['화상'] < 2:
                    enemyStatus['화상'] += 1

            if myTextBox.getStr() == '불덩이작렬':
                if not '화상' in enemyStatus:
                    enemyStatus['화상'] = 0
                if enemyStatus['화상'] < 2:
                    enemyStatus['화상'] += 1
                enemyLeftStunTime += 300
                
            if myTextBox.getStr() == '대규모냉각':
                if not '동상' in enemyStatus:
                    enemyStatus['동상'] = 0
                enemyStatus['동상'] += 1

            if myTextBox.getStr() == '볼트':
                if not '감전' in enemyStatus:
                    enemyStatus['감전'] = 0
                enemyStatus['감전'] += 1

            if myTextBox.getStr() == '체인라이트닝':
                if not '감전' in enemyStatus:
                    enemyStatus['감전'] = 0
                enemyStatus['감전'] += 4
            
            mySkillEffectOffset = global_t
            myTextBox.setStr('')
                
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
            if enemyTextBox.getStr() in enemySkillList:
                enemyMovingInterval = enemySkillCoolDownDictionary[enemyTextBox.getStr()]
                enemyLeftStunTime += enemyMovingInterval
                isEnemyMoving = True
            enemyOffset += enemyTypeInterval + random.randrange(-1 * enemyTypeVarience, enemyTypeVarience + 1)
            enemyIME.resetState()
            enemySkillSet = False

        '''적 타이핑 수행'''
        if global_t - enemyOffset >= enemyTypeInterval:
            c = enemyLetter[enemyCurrIdx]
            keyTuple = enemyIME.getKey(c, True)
            if keyTuple[1]:
                try:
                    enemyTextBox.addStr(keyTuple[0])
                except:
                   pass
            else:
                try:
                    property = enemyTextBox.subStrFromRight(1)
                    enemyTextBox.addStr(keyTuple[0])
                except:
                    pass

            if len(keyTuple) == 4:
                if keyTuple[3]:
                    try:
                        enemyTextBox.addStr(keyTuple[2])
                    except:
                        pass
                else:
                    try:
                        enemyTextBox.subStrFromRight(1)
                        enemyTextBox.addStr(keyTuple[2])
                    except:
                        pass
            enemyOffset += enemyTypeInterval
            enemyCurrIdx += 1

        '''적 행동 완료 체크'''
        if enemyLeftStunTime <= 0 and isEnemyMoving:
            isEnemyMoving = False
            if enemyTextBox.getStr() in enemySkillList:
                myHp -= enemySkillDamageDictionary[enemyTextBox.getStr()]
            enemyTextBox.setStr('')

        '''상태이상'''
        if '화상' in enemyStatus :
            enemyHp -= 0.8 * enemyStatus['화상'] / fps
        if '감전' in enemyStatus:
            if enemyStatus['감전'] >= 5:
                isEnemyMoving = False
                del enemyStatus['감전']
                enemyLeftStunTime += 500
                enemyTextBox.setStr('')
                enemySkillSet = False
        if '동상' in enemyStatus:
            enemyTypeInterval = (2 - (0.8)**enemyStatus['동상']) * enemyTypeIntervalInit

        '''명령어 유효성 체크'''
        myTextBox.checkVaild(mySkillList)
        enemyTextBox.checkVaild(enemySkillList)

        '''무빙 여부 체크'''
        myTextBox.isMoving = isMyMoving
        enemyTextBox.isMoving = isEnemyMoving

        '''입력창 Moving 시 pos 변경'''
        if isMyMoving:
            t = myLeftStunTime / myMovingInterval
            myTextBox.setPos(myTextBox_initX, myTextBox_initY * t**3 + enemyTextBox_initY * (1-t**3))
        else:
            myTextBox.setPos(myTextBox_initX,myTextBox_initY)
        if isEnemyMoving:
            t = enemyLeftStunTime / enemyMovingInterval
            enemyTextBox.setPos(myTextBox_initX, myTextBox_initY * (1-t**3) + enemyTextBox_initY * t**3)
        else:
            enemyTextBox.setPos(myTextBox_initX,enemyTextBox_initY)

        '''화면 출력'''
        screen.fill(pygame.Color("black"))

        '''HP 출력'''
        myHpText = myFont.render("HP : " + str(math.ceil(myHp)), True, (255, 255, 255))
        screen.blit(myHpText, (100, myTextBox_initY))
        enemyHpText = myFont.render("HP : " + str(math.ceil(enemyHp)), True, (255, 255, 255))
        screen.blit(enemyHpText, (100, enemyTextBox_initY))

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
        myScene.draw()

        '''행동 이펙트'''
        if global_t - mySkillEffectOffset < mySkillEffectLifeTime:
            pass

        '''패리 출력'''
        if global_t - myParryTextOffset < myParryTextLifeTime: 
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

        pygame.display.update()

if __name__ == "__main__":
    game()
