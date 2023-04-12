## code from https://github.com/gkdlepdj/PyIME

# 키보드 영어 소문자 -> 한글자모 맵핑 
lower_to_jm = [ 
u"ㅁ",u"ㅠ",u"ㅊ", u"ㅇ",u"ㄷ", u"ㄹ", u"ㅎ", u"ㅗ", u"ㅑ", u"ㅓ", 
u"ㅏ", u"ㅣ", u"ㅡ", u"ㅜ",  u"ㅐ", u"ㅔ", u"ㅂ", u"ㄱ", u"ㄴ", u"ㅅ", 
u"ㅕ", u"ㅍ", u"ㅈ", u"ㅌ", u"ㅛ", u"ㅋ"]
# 키보드 영어 대문자 -> 한글자모 맵핑
upper_to_jm = [ 
u"ㅁ",u"ㅠ", u"ㅊ", u"ㅇ", u"ㄸ", u"ㄹ", u"ㅎ", u"ㅗ",u"ㅑ", u"ㅓ",
u"K" ,u"ㅣ" ,u"ㅡ" ,u"ㅜ" ,u"ㅒ" ,u"ㅖ", u"ㅃ", u"ㄲ",u"ㄴ", u"ㅆ", 
u"ㅕ" ,u"ㅍ" ,u"ㅈ" ,u"ㅌ" ,"ㅛ" ,"ㅋ" ]

# 초성,중성,종성 인덱스 맵핑
CHO_DATA = u"ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ";
JUNG_DATA = u"ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ";
# 종성의 맨 앞빈칸은 종성이 없는 글자의 표현
JONG_DATA = u" ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ";

# 보통 utf-8방식을 선호하나 커맨드창에 한글이 보이게 하기위해 cp949로 인코딩 
ENCODING = 'cp949' 
def isascii(u):
    return ( 0 < ord(u) < 0xff )
    
def isprint(c):
    k = ord(c)
    return ( 0x20<= k <=0x40 ) or ( 0x7b <=k <= 0x7e ) or \
               ( 0x41 <= k <= 0x5a) or ( 0x61 <= k <= 0x7a ) 
    
def is_jaum(u_jm):
    """키보드에서 입력된 자모가 자음인지 판단
    
        소스내에선 선별된 자모를 대상으로 하기때문에 자음이 아니면 모음
    
    @파라미터: u_jm: 유니코드 자모
    @반환: 자음이면 참, 모음이면 거짓 
    """
    return u_jm in CHO_DATA
    
def engkey2kor(c):
    """영어키 변환
    
        영어문자1개 -> 한글자모로 맵핑하여 반환
        
    @파라미터: c: 타입은 스트링형, 변환하고자 하는 문자
    @반환: 영문자에 해당하는 자모, 영대소문자가 아니면 None
    """
    if c.islower():
        return lower_to_jm[ord(c)-97]
    if c.isupper():
        return upper_to_jm[ord(c)-65]
    return None
       
def asm(cho,jung,jong):
    """유니코드 알아내기 
    
        초/중/종성으로 해당 글자의 유니코드를 얻어낸다. 
        유니코드에서 한글 가~힝은 0xAC00~0xD7A3에 대응된다. 
        이는 C언어 배열 3차원 배열로 표현할수 있다. 
            예) unicode[19][21][28] 초성19,중성21,종성28 배열의 시작번지는 AC00
        따라서 초성 중성 종성의 값(인덱스값)을 알면 해당글자의 유니코드를 구할 수 있다.
        
    @파라미터: cho: 타입은 유니코드, 초성 코드
    @파라미터: jung: 타입은 유니코드, 중성 코드
    @파라미터: jong: 타입은 유니코드, 종성 코드
    @반환: 초+중+종에 해당하는 글자의 유니코드 
    """
    dcho = cho.encode(ENCODING) if cho else "*None"
    djung= jung.encode(ENCODING) if jung else "*None"
    djong = jong.encode(ENCODING) if jong else "*None" 
    if cho and not jung and not jong: return cho
    if not cho and jung : return jung    
    idx_cho  = CHO_DATA.find(cho)
    idx_jung = JUNG_DATA.find(jung)
    if jong:
        idx_jong = JONG_DATA.find(jong)
    else:
        idx_jong = 0    
    return chr(idx_cho*21*28 + idx_jung*28 + idx_jong + 0xAC00)

def get_jm(ch):
    '''
    한글 글자를 입력하면 자모를 분리해서 튜플로 리턴하는 함수
    @return: (초성, 중성, 종성)
    '''
    unicode = ord(ch) - 0xAC00
    idx_jong = unicode%28
    unicode = unicode//28
    idx_jung = unicode%21
    unicode = unicode//21
    idx_cho = unicode
    return (CHO_DATA[idx_cho], JUNG_DATA[idx_jung], JONG_DATA[idx_jong])
    

def asm_jm(u_jm1,u_jm2):
    """이중자음/이중모음 유니코드 알아내기 
    
        입력받은 두 자모를 합쳐서 이중모음 또는 이중자음의
        유니코드를 반환한다
        
    @파라미터: u_jm1: 타입은 유니코드,첫번째 자모
    @파라미터: u_jm2: 타입은 유니코드,두번째 자모
    @반환: 이중자모 유니코드 반환 , 해당자모가 없으면 None
    """
    if u_jm1==u"ㅗ" and u_jm2 == u"ㅏ": return u"ㅘ"
    if u_jm1==u"ㅗ" and u_jm2 == u"ㅐ": return u"ㅙ"
    if u_jm1==u"ㅗ" and u_jm2 == u"ㅣ": return u"ㅚ"
    if u_jm1==u"ㅜ" and u_jm2 == u"ㅓ": return u"ㅝ"
    if u_jm1==u"ㅜ" and u_jm2 == u"ㅔ": return u"ㅞ"
    if u_jm1==u"ㅜ" and u_jm2 == u"ㅣ": return u"ㅟ"
    if u_jm1==u"ㅡ" and u_jm2 == u"ㅣ": return u"ㅢ"
    if u_jm1==u"ㄱ" and u_jm2 == u"ㅅ": return u"ㄳ"
    if u_jm1==u"ㄴ" and u_jm2 == u"ㅈ": return u"ㄵ"
    if u_jm1==u"ㄴ" and u_jm2 == u"ㅎ": return u"ㄶ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㄱ": return u"ㄺ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㅁ": return u"ㄻ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㅂ": return u"ㄼ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㅅ": return u"ㄽ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㅍ": return u"ㄿ"
    if u_jm1==u"ㄹ" and u_jm2 == u"ㅎ": return u"ㅀ"
    if u_jm1==u"ㅂ" and u_jm2 == u"ㅅ": return u"ㅄ"
    return None
    

class IME:
    """
    state: 현재의 글자조립상태

            (0)               : 초기상태    
            |                 
            (1)               : 초성입력 상태
            |
            (2) -> (3)        : 중성입력 상태 / 중성 이중모음 상태
            |
            (4) -> (5)        : 종성입력 상태 / 종성 이중자음 상태
    """
    state = 0  
    # 현재 조립중인 초/중/종성 보관
    cho = None
    jung = None 
    jong = None 
    jung1 = None  # 이중모음 첫번째 모음
    jung2 = None  # 이중모음 두번째 모음 
    jong1 = None  #이중자음 첫번째 자음
    jong2 = None  #이중자음 두번째 자음

    def IME(self):
        pass

    def getKey(self,c,isKor):
        '''
        키 입력을 받고 잘 처리해줌
        @c: 입력받은 문자
        @isKor: 입력이 한글인지 여부(한영키 여부)
        @return: (string, boolean) 작성중인 글자, 완료여부(True면 새 글자, False면 이전 글자 변경)를 튜플로 리턴
        * 튜플 길이가 4일 경우, 글자 2개가 한꺼번에 나와야 하는 경우
        '''
        if not isKor:
            # 한글 아니면 기존입력 초기화하고 글자리턴
            self.resetState()
            return (c,True)
        jm = engkey2kor(c)
        if jm == None:
            #자모음이 아니면 초기화하고 글자리턴
            self.resetState()
            return (c,True)
        
        if self.state == 0 : #--------------- 시작상태
            if is_jaum(jm) :
                self.cho = jm         
                self.state = 1
                return (asm(self.cho,self.jung,self.jong),True)
            else :
                self.cho = None
                self.jung = jm
                self.state = 2
                return (asm(self.cho,self.jung,self.jong),True)
        elif self.state == 1 :#--------------- 초성만 완성된 상태
            if is_jaum(jm): #자음이 입력        
                # 글자가 완성되었고 
                #화면에 완성된 글자를 출력하고 
                #다음 글자로 넘어가면서 
                #지금 입력된 글자는 시작이 되어야 한다.            
                self.state = 1
                #input_list.append( cho )
                self.cho=jm; self.jung=None; self.jong=None
                return (asm(self.cho,self.jung,self.jong), True)
            else:
                #모음이 입력됨 
                self.jung = jm
                self.state = 2
                return(asm(self.cho,self.jung,self.jong), False) 
                
        elif self.state == 2 : #--------------- 중성까지 입력된 상태
            if is_jaum(jm):
                if self.cho:
                    # 자음이 들어옴 
                    # 화면에 완성된 글자를 출력하고
                    # 새로 들오온 글자는 자음이므로 
                    # 상태는 4
                    # 종성은 새로들어온 글자할당
                    self.state=4
                    self.jong=jm
                    return(asm(self.cho,self.jung,self.jong), False)
                else:
                    #input_list.append( jung )
                    self.state=1                    
                    self.cho=jm;self.jung=None;self.jong=None
                    return (asm(self.cho,self.jung,self.jong), False)                
            else :      
                #모음이 들어옴 
                new_jm = asm_jm(self.jung,jm)
                if new_jm :  #이중모음 판별
                    self.state = 3 
                    self.jung1=self.jung
                    self.jung2=jm
                    self.jung = new_jm
                    return (asm(self.cho,self.jung,self.jong), False)
                else : #이중모음 x
                    # 새로운 글자가 완성되었고 
                    # 화면에 완성된 글자를 출력하고
                    # 새로 들오온 글자는 모음이므로 
                    # 상태는 2
                    # 초성은 없음
                    # 중성은 현재글자를 할당 
                    # input_list.append( asm(cho,jung,jong) )
                    self.state = 2
                    self.cho = None; self.jung=jm; self.jong=None   
                    return (asm(self.cho,self.jung,self.jong), True)
        elif self.state == 3: #--------------- 중성까지 이중모음이 입력된 상태
            if is_jaum(jm) :
                if self.cho and asm(self.cho,self.jung,jm): #초+중+종으로 한글완성여부 판별 
                    self.state = 4 
                    self.jong = jm
                    return (asm(self.cho,self.jung,self.jong), False)
                else:
                    # 새로운 글자가 완성되었고
                    # 화면에완성된 글자를 출력하고
                    # 새로들어온 글자는 자음이므로
                    # 초성만 할당
                    # 상태는 1
                    # input_list.append( jung )
                    self.state = 1 
                    self.cho=jm; self.jung=None; self.jong=None
                    return (asm(self.cho,self.jung,self.jong), True)                
            else:
                # 새로운 글자가 완성되었고
                # 화면에 완성된 글자를 출력하고 
                # 새로 들어온 글자는 모음이기 때문에  
                # 상태는 2
                # 초성은 없음
                # 중성으 현재글자를 할당 
                # input_list.append( asm(cho,jung,jong) )
                self.state = 2 
                self.cho=None; self.jung=jm; self.jong=None
                return (asm(self.cho,self.jung,self.jong), True)
        elif self.state == 4: #--------------- 종성까지 입력된 상태
            if is_jaum(jm):
                new_jm = asm_jm(self.jong,jm) #종성의 이중자음 가능성 판별
                if new_jm and asm(self.cho,self.jung,self.jong): 
                    # 화면에 완성된 글자를 출력하고
                    # 상태는 5
                    self.jong1=self.jong; self.jong2=jm
                    self.jong=new_jm
                    self.state = 5
                    return (asm(self.cho,self.jung,self.jong), False)
                else:
                    # 새로운 글자가 완성되었고
                    # 화면에 완성된 글자를 출력하고
                    # 자음부터 시작 
                    # 상태는 1
                    # input_list.append( asm(cho,jung,jong) )
                    frontChar = asm(self.cho,self.jung,self.jong)
                    self.state=1 
                    self.cho=jm; self.jung=None; self.jong=None
                    return (frontChar, False ,asm(self.cho,self.jung,self.jong), True)                
            else:    
                # 밍 상태에서 모음이 입력됨
                # 초성 중성으로 글자를 완성 하고
                # 종성 , 모음 -> 초성 중성으로 셋팅
                # 상태는 2로 만들어야 함 
                # input_list.append( asm(cho,jung,None) )
                frontChar = asm(self.cho,self.jung,None)
                self.state=2 
                self.cho=self.jong; self.jung=jm; self.jong=None
                return (frontChar, False,  asm(self.cho,self.jung,self.jong), True)           
        elif self.state == 5: #--------------- 종성 이중자음까지 입력된 상태 
            if is_jaum(jm):
                # 자음이 입력되었음
                # 기존글자는 그대로 두고
                # 새로입력된 자음으로 글자출력
                # 상태는 1
                # input_list.append( asm(cho,jung,jong) )
                self.cho = jm;self.jung = None ;self.jong=None
                self.state=1          
                return (asm(self.cho,self.jung,self.jong), True)
                  
            else:
                # 모음이 입력되었음
                # 초,중,첫번째종성으로 새로운 글자완성 하여 화면에 출력
                # 종성마지막자음과 새로입력된 모음으로 초성중성을 완성
                # 상태는 2
                #input_list.append( asm(cho,jung,jong1) )
                frontChar = asm(self.cho,self.jung,self.jong1)
                self.cho = self.jong2;self.jung = jm ;self.jong=None
                self.state = 2
                return (frontChar, False, asm(self.cho,self.jung,self.jong), True)

    def backSpace(self):
        '''
        backspace를 누르면 호출되는 함수
        @return: string or None. string이면 가장 뒤 글자를 string으로 대체, None이면 글자를 지움
        '''
        
        if self.state==0 :
            # 아무것도 없으므로 걍 지우면된다.
            return None
                
        elif self.state==1:
            # 초성 초기화
            # 상태0
            self.state=0
            self.cho=None
            return None
        elif self.state==2:
            # 상태 1 
            # 중초기화
            self.state=1
            self.jung=None
            if self.cho == None: return None
            return asm(self.cho,self.jung,self.jong)
        elif self.state==3:
            # 상태2 
            self.state=2
            self.jung=self.jung1
            self.jung1=None;self.jung2=None
            return asm(self.cho,self.jung,self.jong)
        elif self.state==4:
            # 상태2
            # 종초기화
            self.state=2
            self.jong=None
            return asm(self.cho,self.jung,self.jong)
        elif self.state==5:
            # 종1종2 초기화
            # 상태4
            # 상태2 
            self.state=4
            self.jong=self.jong1
            self.jung1=None;self.jung2=None
            return asm(self.cho,self.jung,self.jong)

    def resetState(self):
        '''
        IME 클래스의 글자입력 상태를 초기화
        '''
        self.state = 0  
        self.cho = None
        self.jung = None 
        self.jong = None 
        self.jung1 = None  # 이중모음 첫번째 모음
        self.jung2 = None  # 이중모음 두번째 모음 
        self.jong1 = None  #이중자음 첫번째 자음
        self.jong2 = None  #이중자음 두번째 자음
        self.input_list=[]