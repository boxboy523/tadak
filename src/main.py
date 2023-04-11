import pygame
import random

pygame.init()

screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
myFont = pygame.font.SysFont(None, 50)
pygame.display.set_caption("TADAK")


myStr = ''
enemyStr = ''
enemyAtk = ['strike', 'bash', 'slash']
currIdx = -1;
currAtk = ''
atkSet = False

parryStr = ''
canParry = False
parrySuccess = False
parryTime = 0
parryLast = 2000

parryTextTime = 0
parryTextLast = 700

global_t = 0

bspc_t = 0
bspcOffset = 0
enemyOffset = 0

DEL_THRES = 300
#THRES_STUNNED = 1500  # 경직된 글자를 지우는 데 드는 시간.
LATENCY_INIT = 100 # 백스페이스를 꾹 눌렀을 때 지워지는 사이 간격
LATENCY = LATENCY_INIT

enemyTypeInterval = 700

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key not in [pygame.K_BACKSPACE, pygame.K_RETURN]:
                try: myStr += chr(event.key)
                except: pass

    if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # 벡스페이스 누르는 동안 bspc_t 증가
        if bspc_t ==0: myStr = myStr[:len(myStr) - 1]
        bspc_t += 1
    else:
        bspc_t = 0  # 떼면 초기화
        bspcOffset = 0
        LATENCY = LATENCY_INIT

    if pygame.key.get_pressed()[pygame.K_RETURN]:
        if myStr != '':
            parryStr = myStr
            if parryTime > 0 and enemyStr == parryStr:
                parrySuccess = True
                parryTextTime = 1
            if parryTime == 0: parryTime = 1
            myStr = ''

    if len(myStr) > 0:
        if bspc_t - bspcOffset >= DEL_THRES:
            myStr = myStr[:len(myStr) - 1]
            bspcOffset += LATENCY
            LATENCY = max(LATENCY_INIT // 2, LATENCY - 10)

    if not atkSet:
        currIdx = random.randint(0, len(enemyAtk) - 1)
        atkSet = True
        if parryTime > 0 and enemyStr == parryStr:
            parrySuccess = True
            parryTextTime = 1
        if parryTime == 0: parryTime = 1
        enemyStr = '' # 이거 뒤에도 조금 남아있어야 패링이 될듯

    screen.fill(pygame.Color("black"))
    myText = myFont.render(myStr, True, (255, 255, 255))
    enemyText = myFont.render(enemyStr, True, (255, 255, 255))
    parryText = myFont.render("PARRY!!", True, (255, 255, 255))
    prQ = myFont.render(parryStr, True, (255, 255, 255))

    screen.blit(myText, (300, 350))
    screen.blit(enemyText, (350, 150))

    if parryTime > 0:
        #screen.blit(prQ, (200, 150))
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
        if enemyStr == enemyAtk[currIdx]:
            atkSet = False
        enemyStr = enemyAtk[currIdx][:len(enemyStr) + 1]
        enemyOffset += enemyTypeInterval


    global_t += 1
