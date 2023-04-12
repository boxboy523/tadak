import pygame
import random
from textbox import textBox
from ime import IME

DEL_THRES = 300
#THRES_STUNNED = 1500  # 경직된 글자를 지우는 데 드는 시간.
LATENCY_INIT = 100 # 백스페이스를 꾹 눌렀을 때 지워지는 사이 간격
LATENCY = LATENCY_INIT

pygame.init()

def game(): ##페이커는 엄마가 없다.

    screen_width = 800
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("TADAK")

    myFont = pygame.font.SysFont("arial", 50)
    myTextBox = textBox(myFont ,c=(255,255,255))
    enemyTextBox = textBox(myFont, c=(255,255,255))
    enemyStr = ''
    enemyAtk = ['strike', 'bash', 'slash']
    currIdx = -1
    currAtk = ''
    atkSet = False
    gameIME = IME

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
    

    exceptChar = [pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LALT, pygame.K_RALT] # 글자 아닌 키들 분류

    while running:
        shiftPressed = False
        '''값 입력'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key not in exceptChar:
                    gameIME.getKey(event.key)
                    try: myTextBox.addStr(chr(event.key))
                    except: pass
                
                if event.key in [pygame.K_LALT, pygame.K_RALT]:
                    isKor = not isKor
        '''벡스페이스'''
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:  # 벡스페이스 누르는 동안 bspc_t 증가
            if backspace_t ==0: 
                myTextBox.subStr(1)
            backspace_t += 1
        else:
            backspace_t = 0  # 떼면 초기화
            bspcOffset = 0
            LATENCY = LATENCY_INIT
        '''엔터'''
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if myTextBox.getStr() != '':
                parryStr = myTextBox.getStr()
                if parryTime > 0 and enemyTextBox.getStr() == parryStr:
                    parrySuccess = True
                    parryTextTime = 1
                if parryTime == 0: parryTime = 1
                myTextBox.setStr('')
        '''쉬프트'''
        if pygame.key.get_pressed()[pygame.K_LSHIFT, pygame.K_RSHIFT]:
            shiftPressed = True

        

        if myTextBox.getLen() > 0:
            if backspace_t - bspcOffset >= DEL_THRES:
                myTextBox.subStr(1)
                bspcOffset += LATENCY
                LATENCY = max(LATENCY_INIT // 2, LATENCY - 10)

        if not atkSet:
            currIdx = random.randint(0, len(enemyAtk) - 1)
            atkSet = True
            if parryTime > 0 and enemyTextBox.getStr() == parryStr:
                parrySuccess = True
                parryTextTime = 1
            if parryTime == 0: parryTime = 1
            enemyTextBox.setStr('') # 이거 뒤에도 조금 남아있어야 패링이 될듯

        screen.fill(pygame.Color("black"))
        parryText = myFont.render("PARRY!!", True, (255, 255, 255))
        prQ = myFont.render(parryStr, True, (255, 255, 255))

        myTextBox.drawBox(screen,(300,350))
        enemyTextBox.drawBox(screen,(350,150))

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
            if enemyTextBox.getStr() == enemyAtk[currIdx]:
                atkSet = False
            enemyTextBox.setStr(enemyAtk[currIdx][:enemyTextBox.getLen() + 1])
            enemyOffset += enemyTypeInterval


        global_t += 1

'''
class textBox:
    font = pygame.font.SysFont("arial", 50)
    mainStr = ''
    #frontStr = ''
    color = (255,255,255)
    whiteBar = False
    def __init__(self, f, s='', fs='', c=(255,255,255)) -> None:
        self.font = f
        self.mainStr = s
        #self.frontStr =fs
        self.color = c

    def setStr(self,s):
        self.mainStr = s

    def getStr(self):
        return self.mainStr

    def getLen(self):
        return len(self.mainStr)
    
    def setColor(self,c):
        self.color = c

    def subStr(self,i):
        self.mainStr = self.mainStr[:len(self.mainStr)-i]

    def addStr(self,s):
        self.mainStr += s


    def drawBox(self,screen,pos):
        text = self.font.render(self.mainStr, True, self.color)
        pygame.draw.rect(screen, self.color, [pos[0],pos[1],300,self.font.size("a")[1]],4)
        screen.blit(text, pos)
    '''


if __name__ == "__main__":
    game()