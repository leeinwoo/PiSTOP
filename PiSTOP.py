import random

#플레이어 수(init()에서 변경가능)
player = 3

#카드 생성[(1-12월 * 4장) + (와일드카드2장) = 총 50장]
card = [15, 16, 17, 17, 25, 26, 27, 27, 35, 36, 37, 37, 45, 46, 47, 47,
        55, 56, 57, 57, 65, 66, 67, 67, 75, 76, 77, 77, 85, 86, 87, 87,
        95, 96, 97, 97, 105, 106, 107, 107, 115, 116, 117, 117, 125, 126, 127, 128,
        13, 13]

# 플레이어가 손에 쥐고있는 카드 리스트 - 접근 시 player_card[player_index][card_index]
player_card=[[0 for col in range(7)] for row in range(player)]

# 플레이어가 획득한 카드 리스트
player_get_card=[[] for row in range(player)]

# 플레이어가 획득한 점수
player_score=[0,0,0]

# 바닥에 깔려있는 카드
floor_card=[]

# 무덤카드
tomb_card=[]

#플레이어 차례(0~2)
player_turn=0

#카드 섞기
def card_shuffle():
    global card
    random.shuffle(card)
    print ("shuffle card : %s\n\n" % card)

#카드 분배 (player card 7장씩 인원 만큼 분배 후 floor card 6장)
def card_share():
    for j in range(player): # 플레이어 카드 분배
        for i in range(7):
            global player_card            
            player_card[j][i] = card.pop()
        print("player%d : %s" % (j+1, player_card[j]))
        print("\n")
    while 1: # 바닥 카드 분배
        global floor_card        
        if(len(floor_card)==6):
            break
        else:
            temp_card = card.pop()
            if(temp_card == 13): # 바닥에 와일드 카드가 깔린 경우
                player_get_card[player_turn].append(13) # 첫 번째 차례 플레이어에게 준다
            else:
                floor_card.append(temp_card)
    for n in range(len(card)): # 무덤 카드 분배
        global tomb_card
        tomb_card.append(card.pop())

#카드 정렬 (플레이어 카드, 바닥 카드)
def card_sort():
    for i in range(player):        
        player_card[i].sort()
        player_get_card[i].sort()
    floor_card.sort()
    print("무덤 카드 목록 : %s\n" % tomb_card)
    print("바닥 카드 목록 : %s\n" % floor_card)
    print("%d번 플레이어 손 카드 목록 : %s\n" % (player_turn+1, player_card[player_turn]))
    print("%d번 플레이어 획득 카드 목록 : %s\n" % (player_turn+1, player_get_card[player_turn]))

#게임 시작
def start_game():
    global player_turn
    for i in range(7*player):
        get_throw_card()
        print("%d번 플레이어 손 카드 목록 : %s\n" % (player_turn+1, player_card[player_turn]))
        print("%d번 플레이어 획득 카드 목록 : %s\n" % (player_turn+1, player_get_card[player_turn]))
        player_turn += 1
        if(player_turn>=3):
            player_turn=0
            return
        card_sort()
#카드 내기
def get_throw_card():
    get_player_card=0    
    print("%d번 플레이어 차례입니다!\n" % (player_turn+1))
    get_player_card = input("카드를 내세요 : ")
    get_player_card = int(get_player_card)
    if(get_player_card==13): # 와일드 카드를 냈을 경우
        player_get_card[player_turn].append(13) # 플레이어가 획득 하고
        player_card[player_turn].append(tomb_card.pop()) # 무덤 카드에서 손으로 한장 들고 온다
        player_card[player_turn].remove(get_player_card) # 낸 카드 삭제
        print("\n카드를 뒤집었습니다\n\n남은 무덤 카드 수 : %d\n" % len(tomb_card))
        print("%d번 플레이어 손 카드 목록 : %s\n" % (player_turn+1, player_card[player_turn]))
        get_throw_card()
    else: # 와일드 카드가 아닌 경우
        decide_card(get_player_card) # 카드 판정
        player_card[player_turn].remove(get_player_card)
        
# 바닥 카드 리스트와 일치 비교연산
def cmp_card_list(card):
    global floor_card
    match_count=0 # 바닥 카드와 일치하는 수
    match_num=[] # 낸 카드와 일치하는 바닥 카드 - 판정이 끝난 뒤 추가/삭제 연산을 위해
    for i in range(len(floor_card)):
        if(abs(int(card) - floor_card[i]) < 4): # 차가 4 미만이면 같은 카드
            match_num.append(floor_card[i])
            match_count += 1
    return match_count, match_num
#카드 판정
def decide_card(get_player_card):
    get_player_card = int(get_player_card)
    match_count=0 # '낸 카드'와 일치하는 '바닥 카드' 수
    match_num=[] # '낸 카드' 일치하는 '바닥 카드' 리스트 - 판정이 끝난 뒤 추가/삭제 연산을 위해
    match_count2=0 # '무덤에서 뒤집은 카드'와 일치하는 '바닥 카드' 수
    match_num2=[] # '무덤에서 뒤집은 카드'와 일치하는 '바닥 카드' 리스트 - 판정이 끝난 뒤 추가/삭제 연산을 위해
    draw_card=0 # 무덤에서 뒤집어 나온 카드
    wild_card=0 # 뒤집어서 나온 와일드 카드 수

    match_count, match_num = cmp_card_list(get_player_card)

    draw_card = draw_tombcard() # 카드 뒤집기    
    for i in range(2):        
        if(draw_card == 13): #와일드 카드 일 때
            wild_card += 1
            draw_card = draw_tombcard() # 한 장 더 뒤집음
        else:
            break;
    match_count2, match_num2 = cmp_card_list(draw_card)
            
    if(match_count==1): # 바닥카드와 1개가 일치할 때 - 무덤카드를 뒤집어보고 같은 카드가 나오지 않으면(안 쌌을때) 가져감
        if(match_count2==0): # 뒤집은 카드와 일치하는 카드가 없을 때
            player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
            player_get_card[player_turn].append(get_player_card)
            floor_card.remove(match_num[0]) # 가져간 카드 삭제
            floor_card.append(draw_card) # 뒤집은 카드는 바닥에 놓음
        elif(match_count2==1): # 뒤집은 카드와 일치하는 카드가 1장 일 때
            if(abs(get_player_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 일치하는 경우(쌌을 경우)
                print("쌌다\n")
                # 카드를 모두 바닥에 놓는다
                floor_card.append(get_player_card)
                floor_card.append(draw_card)
                for i in range(wild_card):
                    floor_card.append(13)
                wild_card=0
            else: # 뒤집은 카드가 다른 바닥카드와 일치하는 경우(안 싼 경우)
                player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(match_num2[0]) # 무덤에서 뒤집은 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(draw_card)                
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
        elif(match_count2==2): # 뒤집은 카드와 일치하는 카드가 2장 일 때
            if(match_num2[0] == match_num2[1]): # 일치하는 바닥카드 2장이 같은 모양일 경우
                player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(match_num2[0]) # 뒤집은 카드 + 일치하는 아무 카드 1장 가져간다
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
            else: # 일치하는 바닥카드 2장이 다른 모양일 경우
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_player_card)
                #사용자가 가져갈 카드를 선택한다                
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(choice)
        elif(match_count2==3): # 뒤집은 카드와 일치하는 카드가 3장 일 때
            player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
            player_get_card[player_turn].append(get_player_card)
            player_get_card[player_turn].append(match_num2[0]) # 뒤집은 카드 + 일치하는 카드 3장을 모두 가져간다
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            player_get_card[player_turn].append(draw_card)
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            
    elif(match_count==2): # 바닥카드와 2개가 일치할 때 - 무덤카드를 뒤집어보고 같은 카드가 나오지 않으면 가져갈 카드 선택
                                                         #같은 카드가 나온 경우 모두 가져가고 각 플레이어들에게 피 1장씩 받음
        if(match_count2==0): # 뒤집은 카드와 일치하는 카드가 없을 때
            if(match_num[0] == match_num[1]): # 일치하는 바닥카드 2장이 같은 모양일 경우
                player_get_card[player_turn].append(match_num[0]) # 낸 카드 + 일치하는 아무 카드 1장 가져간다
                player_get_card[player_turn].append(get_player_card)                
                floor_card.append(draw_card) # 뒤집은 카드는 바닥에 놓음
                floor_card.remove(match_num[0])
            else: # 일치하는 바닥카드 2장이 다른 모양일 경우
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(get_player_card)  
                floor_card.append(draw_card)
                floor_card.remove(choice)
        elif(match_count2==1): # 뒤집은 카드와 일치하는 카드가 1장 일 때
            if(match_num[0] == match_num[1]): 
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
            else:
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(draw_card)  
                floor_card.remove(choice)
                floor_card.remove(match_num2[0])
        elif(match_count2==2): # 뒤집은 카드와 일치하는 카드가 2장 일 때
            if(abs(get_player_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 일치하는 경우(따닥)
                print("따닥\n")
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(match_num[1])
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num[1])
                #각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            else: # 낸 카드와 뒤집은 카드가 일치하지 않는 경우(따닥이 아닌 경우)
                if(match_num[0] == match_num[1]):  # 같은 모양(1st)
                    if(match_num2[0] == match_num2[1]): # 같은 모양(2nd)
                        player_get_card[player_turn].append(match_num[0])
                        player_get_card[player_turn].append(get_player_card)
                        player_get_card[player_turn].append(match_num2[0])
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(match_num[0])
                        floor_card.remove(match_num2[0])
                    else: # 다른 모양(2nd)
                        player_get_card[player_turn].append(match_num[0])
                        player_get_card[player_turn].append(get_player_card)
                        choice = choice_card(match_num2[0], match_num2[1])
                        player_get_card[player_turn].append(choice)                       
                        player_get_card[player_turn].append(draw_card)  
                        floor_card.remove(choice)
                        floor_card.remove(match_num[0])
                else: # 다른 모양(1st)                    
                    if(match_num2[0] == match_num2[1]): # 같은 모양(2nd)
                        choice = choice_card(match_num[0], match_num[1])
                        player_get_card[player_turn].append(choice)
                        player_get_card[player_turn].append(get_player_card)
                        player_get_card[player_turn].append(match_num2[0])
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(choice)
                        floor_card.remove(match_num2[0])
                    else: # 다른 모양(2nd)
                        choice1 = choice_card(match_num[0], match_num[1])
                        player_get_card[player_turn].append(choice1)
                        player_get_card[player_turn].append(get_player_card)
                        choice2 = choice_card(match_num2[0], match_num2[1])
                        player_get_card[player_turn].append(choice2)
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(choice1)
                        floor_card.remove(choice2)
                        
        elif(match_count2==3): # 뒤집은 카드와 일치하는 카드가 3장 일 때
            if(match_num[0] == match_num[1]):
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_player_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(match_num2[1])
                player_get_card[player_turn].append(match_num2[2])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                floor_card.remove(match_num2[1])
                floor_card.remove(match_num2[2])
                # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            else:
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(match_num2[1])
                player_get_card[player_turn].append(match_num2[2])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                floor_card.remove(match_num2[1])
                floor_card.remove(match_num2[2])
                floor_card.remove(choice)
                # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
                
    elif(match_count==3): # 바닥카드와 3개가 일치할 때 - 모두 가져가고 각 플레이어들에게 피 1장씩 받음
        print("싼거 먹었다\n")
        player_get_card[player_turn].append(get_player_card)
        player_get_card[player_turn].append(match_num[0])
        player_get_card[player_turn].append(match_num[1])
        player_get_card[player_turn].append(match_num[2])
        floor_card.remove(match_num[0])
        floor_card.remove(match_num[1])
        floor_card.remove(match_num[2])
        # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
        if(match_count2==0):
            floor_card.append(draw_card)
        elif(match_count2==1):
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(draw_card)
            floor_card.remove(match_num2[0])
        elif(match_count2==2):
            if(match_num2[0] == match_num2[1]):
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
            else:
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(choice)
        elif(match_count2==3):
            player_get_card[player_turn].append(draw_card)
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)    
    else: # 바닥카드와 일치하지 않을 때        
        if(match_count2==0):
            floor_card.append(get_player_card)
            floor_card.append(draw_card)
        elif(match_count2==1):
            if(abs(get_player_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 같은 경우(쪽)
                print("쪽\n")
                player_get_card[player_turn].append(draw_card)
                player_get_card[player_turn].append(get_player_card)
                # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            else: # 낸 카드와 뒤집은 카드가 같지 않은 경우(쪽이 아닌 경우)
                floor_card.append(get_player_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
        elif(match_count2==2):
            if(match_num2[0] == match_num2[1]):
                floor_card.append(get_player_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
            else:
                floor_card.append(get_player_card)
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(draw_card)
                player_get_card[player_turn].append(choice)
                floor_card.remove(choice)
        elif(match_count2==3):
            floor_card.append(get_player_card)
            player_get_card[player_turn].append(draw_card)
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)    
    for i in range(wild_card): # 뒤집어서 나온 와일드 카드를 모두 가져온다(싼 경우 제외)
        player_get_card[player_turn].append(13)
#카드 2장 중 가져갈 카드를 선택해야 하는 경우
def choice_card(select1, select2):
    choice = input("[%d, %d] 중 가져 갈 카드를 선택하세요 : " % (select1, select2))
    choice = int(choice)
    return choice

#상대방의 피 1장 가져온다(있을 경우에만)
#def rob_card():

#무덤카드 뒤집기
def draw_tombcard():
    global tomb_card
    tombcard=tomb_card[0]
    tomb_card.remove(tomb_card[0])
    print("\n카드를 뒤집었습니다\n\n남은 무덤 카드 수 : %d\n" % len(tomb_card))
    print("뒤집은 카드 : %d\n" % tombcard)
    return tombcard

#점수 계산
def calculate_score(player_num, september_state):
    global player_get_card
    global player_score
    blood_list = [[17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117], [13, 116, 128]] #[[피],[쌍피]] - 10장부터 장당 1점
    band_list = [[16, 26, 36], [66, 96, 106], [46, 56, 76], [127]] #[[홍단],[청단],[초단],[띠]] - 홍단,청단,초단: 3점, 띠: 5장부터 장당 1점
    animal_list = [[25, 45, 86], [55, 65, 75, 105, 126]] #[[고도리],[동물]] - 고도리: 5점, 동물: 5장부터 장당 1점, 7개: 멍텅구리(점수x2)
    light_list = [[15, 35, 85, 115], [125]] #[[광],[비광]] - 3광: 3점(단, 비광포함 시 2점), 5광: 15점
    blood_count=0
    band_count=[0,0,0,0]
    animal_count=[0,0]
    light_count=[0,0]
    score_double=0
    if(september_state==0): #9월(95번)을 피로 처리
        blood_list[1].append(95)
    else: #9월(95번)을 동물로 처리
        animal_list[1].append(95)

    #임시 처리
    player_get_card[player_num] = [13, 13, 95, 17, 27, 37, 47, 57, 57, 35, 85, 125, 66, 36, 26, 16, 86, 45, 25, 126, 105, 75, 65, 55]
   
    for j in range(len(player_get_card[player_num])):
        blood_count += blood_list[0].count(player_get_card[player_num][j]) #피
        blood_count += (blood_list[1].count(player_get_card[player_num][j]) * 2) #쌍피
        band_count[0] += band_list[0].count(player_get_card[player_num][j]) #홍단
        band_count[1] += band_list[1].count(player_get_card[player_num][j]) #청단
        band_count[2] += band_list[2].count(player_get_card[player_num][j]) #초단
        band_count[3] += band_list[3].count(player_get_card[player_num][j]) #띠
        animal_count[0] += animal_list[0].count(player_get_card[player_num][j]) #고도리
        animal_count[1] += animal_list[1].count(player_get_card[player_num][j]) #동물
        light_count[0] += light_list[0].count(player_get_card[player_num][j]) #광
        light_count[1] += light_list[1].count(player_get_card[player_num][j]) #비광

    if(blood_count >= 10):
        player_score[player_num] += blood_count-9 #피 점수
        print("피 점수: %d " % (blood_count-9))
    if(band_count[0] == 3):
        player_score[player_num] += 3 #홍단
        print("홍단 ")
    if(band_count[1] == 3):
        player_score[player_num] += 3 #청단
        print("청단 ")
    if(band_count[2] == 3):
        player_score[player_num] += 3 #초단
        print("초단 ")
    band_sum = band_count[0] + band_count[1] + band_count[2]
    if(band_sum >= 5):
        player_score[player_num] +=  band_sum-4 #띠 점수
        print("띠 점수 : %d " % (band_sum-4))
    if(animal_count[0] == 3):
        player_score[player_num] += 5 #고도리
        print("고도리 ")
    animal_sum = animal_count[0] + animal_count[1]
    if(animal_sum >= 5):
        player_score[player_num] +=  animal_sum-4 #동물 점수
        print("동물 점수 : %d " % (animal_sum-4))
        if(animal_sum>=7):
            score_double += 1 #멍텅구리(점수x2배)
            print("멍텅구리 ")
    light_sum = light_count[0] + light_count[1]
    
    if(light_sum == 3): #3광
        if(light_count[1]==1): #비광 포함
            player_score[player_num] += 2
            print("3비+광 ")
        else: #비광 비포함
            player_score[player_num] += 3
            print("3광 ")
    elif(light_sum == 4): #4광
        player_score[player_num] += 4
        print("4광 ")
    elif(light_sum == 5): #5광
        player_score[player_num] += 15
        print("5광 ")
    if(score_double != 0):
        player_score[player_num] *= pow(2,score_double)
        print("더블 : %d " % score_double)

    print("%d player score : %s\n" % (player_num+1, player_score[player_num]))

#초기화
def init():
    global player
    global player_turn
    player = 3
    player_turn = 0
    card_shuffle()
    card_share()
    card_sort()

#print(len(player_get_card[0]))
init()
start_game()
calculate_score(0,0)
