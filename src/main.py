import pygame
import random
from textbox import textBox
from ime import IME

DEL_THRES = 300
# THRES_STUNNED = 1500  # 경직된 글자를 지우는 데 드는 시간.
LATENCY_INIT = 100  # 백스페이스를 꾹 눌렀을 때 지워지는 사이 간격
LATENCY = LATENCY_INIT

pygame.init()


def game():  ##페이커는 엄마가 없다.

    screen_width = 800
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TADAK")

    myFont = pygame.font.SysFont("Nanum Gothic", 50)
    myTextBox = textBox(myFont)
    enemyTextBox = textBox(myFont)
    enemyStr = ''
    enemyAtk = ['strike', 'bash', 'slash']
    currIdx = -1
    currAtk = ''
    atkSet = False
    gameIME = IME()

    parryStr = ''
    canParry = False
    parrySuccess = False
    parryTime = 0
    parryLast = 2000

    parryTextTime = 0
    parryTextLast = 700

    global_t = 0

    backspace_t = 0
    bspcOffset = 0
    enemyOffset = 0

    enemyTypeInterval = 700

    running = True
    isKor = True
    shiftPressed = False

    exceptChar = [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LALT,
                  pygame.K_RALT]  # 글자 아닌 키들 분류

    while running:
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
                    try:
                        c = chr(event.key)
                        if shiftPressed and (97 <= ord(c) <= 122):
                            c = c.upper()
                        keyTuple = gameIME.getKey(c, isKor)
                        if (keyTuple[1]):
                            try:
                                myTextBox.addMainStr(keyTuple[0])
                            except:
                                pass
                        else:
                            try:
                                myTextBox.subMainStrFromRight(1)
                                myTextBox.addMainStr(keyTuple[0])
                            except:
                                pass

                        if (len(keyTuple) == 4):
                            if (keyTuple[3]):
                                try:
                                    myTextBox.addMainStr(keyTuple[2])
                                except:
                                    pass
                            else:
                                try:
                                    myTextBox.subMainStrFromRight(1)
                                    myTextBox.addMainStr(keyTuple[2])
                                except:
                                    pass
                    except:
                        pass

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    shiftPressed = False
        '''벡스페이스'''
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # 벡스페이스 누르는 동안 bspc_t 증가
            if backspace_t == 0:
                bsp = gameIME.backSpace()
                myTextBox.subMainStrFromRight(1)
                if bsp != None:
                    myTextBox.addMainStr(bsp)
            backspace_t += 1
        else:
            backspace_t = 0  # 떼면 초기화
            bspcOffset = 0
            LATENCY = LATENCY_INIT
        '''엔터'''
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if myTextBox.getMainStr() != '':
                parryStr = myTextBox.getMainStr()
                if parryTime > 0 and enemyTextBox.getMainStr() == parryStr:
                    parrySuccess = True
                    parryTextTime = 1
                if parryTime == 0: parryTime = 1
                myTextBox.setMainStr('')
        '''쉬프트'''
        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
            shiftPressed = True

        if myTextBox.getMainStr() != '':
            if backspace_t - bspcOffset >= DEL_THRES:
                myTextBox.subMainStrFromRight(1)
                bspcOffset += LATENCY
                LATENCY = max(LATENCY_INIT // 2, LATENCY - 10)

        if not atkSet:
            currIdx = random.randint(0, len(enemyAtk) - 1)
            atkSet = True
            if parryTime > 0 and enemyTextBox.getMainStr() == parryStr:
                parrySuccess = True
                parryTextTime = 1
            if parryTime == 0: parryTime = 1
            enemyTextBox.setMainStr('')  # 이거 뒤에도 조금 남아있어야 패링이 될듯

        screen.fill(pygame.Color("black"))
        parryText = myFont.render("PARRY!!", True, (255, 255, 255))
        prQ = myFont.render(parryStr, True, (255, 255, 255))

        myTextBox.drawBox(screen, (300, 350))
        enemyTextBox.drawBox(screen, (350, 150))

        if parryTime > 0:
            # screen.blit(prQ, (200, 150))
            parryTime += 1
        if parryTime > parryLast:
            parryTime = 0
            parryStr = ''

        if parryTextTime > 0:
            screen.blit(parryText, (350, 250))
            parryTextTime += 1
        if parryTextTime > parryTextLast: parryTextTime = 0

        pygame.display.update()

        if global_t - enemyOffset >= enemyTypeInterval:
            if enemyTextBox.getMainStr() == enemyAtk[currIdx]:
                atkSet = False
            enemyTextBox.setMainStr(enemyAtk[currIdx][:enemyTextBox.getMainLen() + 1])
            enemyOffset += enemyTypeInterval

        global_t += 1


if __name__ == "__main__":
    game()
