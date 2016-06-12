import random, sys, threading, time
from PiSTOP_Server_GUI import *
from PiSTOP_Server_Socket import *
from PiSTOP_Sound import *

player = 3 #플레이어 수(init()에서 변경가능)

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

# 플레이어의 이전점수(고 상태일 때 다음 고/스톱 여부 결정을 위해 필요)
player_prev_score=[0,0,0]

# 플레이어의 GO 횟수
player_go_count=[0,0,0]

# 플레이어의 흔들기 횟수
player_shake_count=[0,0,0]

# 플레이어의 [피박, 광박] 여부
player_oneself=[[False,False],[False,False],[False,False]]

# 플레이어의 9월 카드 상태 -> 95번 카드는 쌍피/동물 선택적 사용
september_choice = [False,False,False] #True: 쌍피, False: 동물

# 바닥에 깔려있는 카드
floor_card=[]

# 무덤카드
tomb_card=[]

# 싼 카드 갯수, 리스트(싼 카드번호,와일드카드 갯수) - 와일드 카드와 같이 묶여있는 경우 때문에 필요
pee_count=0
pee_card=[[] for row in range(10)]

#플레이어 차례(0~2)
player_turn=0



#게임 초기화 작업
def init():
    global player, player_turn, card, client
    card = [15, 16, 17, 17, 25, 26, 27, 27, 35, 36, 37, 37, 45, 46, 47, 47,
        55, 56, 57, 57, 65, 66, 67, 67, 75, 76, 77, 77, 85, 86, 87, 87,
        95, 96, 97, 97, 105, 106, 107, 107, 115, 116, 117, 117, 125, 126, 127, 128,
        13, 13]
    player = 3
    player_turn = 0
    while 1:
        if(get_client()==3):# 3명이 접속하면 게임을 시작함
            time.sleep(0.5)
            print("게임이 곧 시작됩니다!\n")
            reset_gui()
            time.sleep(3)
            card_shuffle()
            card_share()
            update_card_image(0, player_get_card[0])
            update_card_image(1, player_get_card[1])
            update_card_image(2, player_get_card[2])
            break

#게임 시작
def game_start():
    set_filename("starting")
    threading._start_new_thread(play_sound,())
    init()
    global player_turn
    for i in range(7*player):
        is_connect()
        print("바닥 카드 : %s\n" % floor_card)
        print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
        set_turn_image(player_turn)
        throw_card()
        update_card_image(player_turn, player_get_card[player_turn])
        card_sort()
        calculate_score(player_turn, september_choice[player_turn])
        if(player_score[player_turn] >= 3): # 플레이어 점수가 3점 이상이면
            if(player_go_count[player_turn] >= 1): # 고 상태일 경우(이전 점수랑 비교해서 1점이상 획득해야 고/스톱 가능)
                if(player_score[player_turn] - player_prev_score[player_turn] >= 1):
                    choice_go_stop(player_turn) # 고/스톱 여부 결정
                    set_filename("go_stop")
                    threading._start_new_thread(play_sound,())
            else: # 고 상태가 아닐 경우
                choice_go_stop(player_turn) # 고/스톱 여부 결정
        player_turn += 1
        if(player_turn>=player):
            player_turn=0
#카드 섞기
def card_shuffle():
    global card
    random.shuffle(card)
    set_filename("card_shuffle")
    threading._start_new_thread(play_sound,())
    print ("\n카드를 섞는 중입니다...\n")
    print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

#카드 분배 (player card 7장씩 인원 만큼 분배 후 floor card 6장)
def card_share():
    global player_card
    global floor_card
    global tomb_card
    player_card.clear()
    player_card=[[0 for col in range(7)] for row in range(player)]
    print ("\n카드를 분배하는 중입니다...\n")
    for j in range(player): # 플레이어 카드 분배
        for i in range(7):            
            player_card[j][i] = card.pop()
    for j in range(player):        
        for i in range(7):
            hand_count=0
            for k in range(7):
                if(abs(player_card[j][i] - player_card[j][k]) < 4):
                    hand_count += 1
            if(hand_count==4):
                print("%d번 플레이어가 총통입니다!\n" % (j+1))
                game_start()
    floor_card.clear()
    while 1: # 바닥 카드 분배        
        if(len(floor_card)==6):
            break
        else:
            temp_card = card.pop()            
            
            if(temp_card == 13): # 바닥에 와일드 카드가 깔린 경우
                player_get_card[player_turn].append(13) # 첫 번째 차례 플레이어에게 준다
            else:
                floor_card.append(temp_card)
                set_card_image("floor",temp_card)
        for i in range(len(floor_card)):
            floor_count=0
            for j in range(len(floor_card)):
                if(abs(floor_card[i] - floor_card[j]) < 4):
                    floor_count += 1
            if(floor_count==4):
                print("총통입니다!\n")
                game_start()
            elif(floor_count==3):
                pee_card[pee_count].append(floor_card[i])
                pee_card[pee_count].append(0)
    floor_card.sort()
    tomb_card.clear()
    for n in range(len(card)): # 무덤 카드 분배        
        tomb_card.append(card.pop())            

#카드 정렬 (플레이어 카드, 바닥 카드)
def card_sort():
    for i in range(player):        
        player_card[i].sort()
        player_get_card[i].sort()
    floor_card.sort()
    for j in range(player): # 각 클라이언트에게 손패 리스트 전달 (command : hand)
        send_msg("hand",player_card[j],j)
    print("획득 카드 : %s\n" % (player_get_card[player_turn]))
    print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

#카드 내기
def throw_card():
    match_count=0
    match_num=[]
    match_count2=0
    match_num2=[]
    temp_shake = []
    get_throw_card=0
    hand_count=1
    print("%d번 플레이어 차례입니다!\n" % (player_turn+1))
    card_sort()
    send_msg("turn",player_turn,player_turn)
    get_throw_card = int(recv_msg(player_turn))
    player_card[player_turn].remove(get_throw_card)
    #get_throw_card = input("카드를 내세요 : ") #original code
    #get_throw_card = player_card[player_turn].pop() # test code
    #get_throw_card = int(get_throw_card) #pre version code        
    
    if(get_throw_card==13): # 와일드 카드를 냈을 경우
        player_get_card[player_turn].append(13) # 플레이어가 획득 하고
        update_card_image(player_turn, player_get_card[player_turn])
        player_card[player_turn].append(tomb_card.pop()) # 무덤 카드에서 손으로 한장 들고 온다        
        print("\n카드를 뒤집었습니다\n")
        card_sort()
        throw_card()
    else: # 와일드 카드가 아닌 경우        
        for i in range(len(player_card[player_turn])):
            if(abs(get_throw_card - player_card[player_turn][i]) < 4):
                temp_shake.append(player_card[player_turn][i])
                hand_count += 1
        if(hand_count==3): # 같은 카드를 3장 들고있는 경우
            match_count, match_num = cmp_card_list(get_throw_card)
            if(match_count==1): # 바닥에 일치하는 카드가 있는 경우 - 흔들면서 폭탄
                set_filename("bomb")
                threading._start_new_thread(play_sound,())
                player_shake_count[player_turn] += 1
                player_get_card[player_turn].append(match_num[0])
                temp_card1 = temp_shake.pop()
                player_get_card[player_turn].append(temp_card1)
                set_card_image("floor", temp_card1) #!
                temp_card2 = temp_shake.pop()
                player_get_card[player_turn].append(temp_card2)
                set_card_image("floor", temp_card2) #!
                player_get_card[player_turn].append(get_throw_card)              
                set_card_image("floor", get_throw_card) #!
                floor_card.remove(match_num[0])                
                
                rob_card(player_turn)
                draw_card = draw_tombcard() # 카드 뒤집기    
                for i in range(2):        
                    if(draw_card == 13): #와일드 카드 일 때
                        player_get_card[player_turn].append(13)
                        draw_card = draw_tombcard() # 한 장 더 뒤집음                        
                    else:
                        break;
                match_count2, match_num2 = cmp_card_list(draw_card)
                set_card_image("floor", draw_card) #!
                if(match_count2==0):
                    print("(4,0)\n")
                    floor_card.append(draw_card)                    
                elif(match_count2==1):
                    print("(4,1)\n")
                    player_get_card[player_turn].append(match_num2[0])
                    player_get_card[player_turn].append(draw_card)
                    floor_card.remove(match_num2[0])                    
                    time.sleep(1) #!                   
                    remove_card_image("floor", draw_card) #!
                    remove_card_image("floor", match_num2[0]) #!                    
                elif(match_count2==2):
                    if(match_num2[0] == match_num2[1]):
                        print("아무거나(4,2)\n")
                        player_get_card[player_turn].append(match_num2[0])
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(match_num2[0])                                               
                        time.sleep(1) #!
                        remove_card_image("floor", draw_card) #!
                        remove_card_image("floor", match_num2[0]) #!                        
                    else:
                        print("선택(4,2)\n")
                        choice = choice_card(match_num2[0], match_num2[1])
                        player_get_card[player_turn].append(choice)
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(choice)                        
                        time.sleep(1) #!
                        remove_card_image("floor", draw_card) #!
                        remove_card_image("floor", choice) #! 
                elif(match_count2==3):
                    print("싼거 또 먹음(4,3)\n")
                    get_pee_wild_card(draw_card)
                    player_get_card[player_turn].append(draw_card)
                    player_get_card[player_turn].append(match_num2[0])
                    player_get_card[player_turn].append(match_num2[1])
                    player_get_card[player_turn].append(match_num2[2])
                    floor_card.remove(match_num2[0])
                    floor_card.remove(match_num2[1])
                    floor_card.remove(match_num2[2])
                    rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)                 
                    time.sleep(1) #!
                    remove_card_image("floor", draw_card) #!
                    remove_card_image("floor", match_num2[0]) #!
                    remove_card_image("floor", match_num2[1]) #!
                    remove_card_image("floor", match_num2[2]) #!
                remove_card_image("floor", temp_card1)
                remove_card_image("floor", temp_card2)
                remove_card_image("floor", get_throw_card)
                remove_card_image("floor", match_num[0]) #!
            else: # 바닥에 일치하는 카드가 없는 경우 - 흔들기 여부 선택
                choice_shake(player_turn)
                decide_card(get_throw_card) # 카드 판정
        else:
            decide_card(get_throw_card) # 카드 판정
            #player_card[player_turn].remove(get_throw_card) #original code
        
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
def decide_card(get_throw_card):
    global pee_card, pee_count
    get_throw_card = int(get_throw_card)
    match_count=0 # '낸 카드'와 일치하는 '바닥 카드' 수
    match_num=[] # '낸 카드' 일치하는 '바닥 카드' 리스트 - 판정이 끝난 뒤 추가/삭제 연산을 위해
    match_count2=0 # '무덤에서 뒤집은 카드'와 일치하는 '바닥 카드' 수
    match_num2=[] # '무덤에서 뒤집은 카드'와 일치하는 '바닥 카드' 리스트 - 판정이 끝난 뒤 추가/삭제 연산을 위해
    draw_card=0 # 무덤에서 뒤집어 나온 카드
    wild_card=0 # 뒤집어서 나온 와일드 카드 수

    match_count, match_num = cmp_card_list(get_throw_card)
        
    draw_card = draw_tombcard() # 카드 뒤집기    
    for i in range(2):        
        if(draw_card == 13): #와일드 카드 일 때
            wild_card += 1
            draw_card = draw_tombcard() # 한 장 더 뒤집음
        else:
            break;
    match_count2, match_num2 = cmp_card_list(draw_card)

    set_card_image("floor", get_throw_card)
    set_card_image("floor", draw_card)
    
    if(match_count==1): # 바닥카드와 1개가 일치할 때 - 무덤카드를 뒤집어보고 같은 카드가 나오지 않으면(안 쌌을때) 가져감
        if(match_count2==0): # 뒤집은 카드와 일치하는 카드가 없을 때
            print("(1,0)\n")
            player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
            player_get_card[player_turn].append(get_throw_card)
            floor_card.remove(match_num[0]) # 가져간 카드 삭제
            floor_card.append(draw_card) # 뒤집은 카드는 바닥에 놓음
            remove_card_image("floor", match_num[0])
            remove_card_image("floor", get_throw_card)
        elif(match_count2==1): # 뒤집은 카드와 일치하는 카드가 1장 일 때
            if(abs(get_throw_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 일치하는 경우(쌌을 경우)
                print("쌌음\n")
                set_filename("puck")
                threading._start_new_thread(play_sound,())
                # 카드를 모두 바닥에 놓는다
                floor_card.append(get_throw_card)
                floor_card.append(draw_card)
                for i in range(wild_card):
                    set_card_image("floor", 13, loNum=int(get_throw_card/10))
                    floor_card.append(13)
                pee_card[pee_count].append(get_throw_card)
                pee_card[pee_count].append(wild_card)
                pee_count += 1
                wild_card=0
                #!!!
            else: # 뒤집은 카드가 다른 바닥카드와 일치하는 경우(안 싼 경우)
                print("(1,1)\n")
                player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0]) # 무덤에서 뒤집은 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(draw_card)                
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
                remove_card_image("floor", get_throw_card)
        elif(match_count2==2): # 뒤집은 카드와 일치하는 카드가 2장 일 때
            if(match_num2[0] == match_num2[1]): # 일치하는 바닥카드 2장이 같은 모양일 경우
                print("아무카드나 가져옴(1,2)\n")
                player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0]) # 뒤집은 카드 + 일치하는 아무 카드 1장 가져간다
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
                remove_card_image("floor", get_throw_card)
            else: # 일치하는 바닥카드 2장이 다른 모양일 경우
                print("선택해서 가져옴(1,2)\n")
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_throw_card)
                #사용자가 가져갈 카드를 선택한다
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(choice)
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", choice)
                remove_card_image("floor", draw_card)
                remove_card_image("floor", get_throw_card)
        elif(match_count2==3): # 뒤집은 카드와 일치하는 카드가 3장 일 때
            print("싼거 먹음(1,3)\n")
            get_pee_wild_card(draw_card)
            player_get_card[player_turn].append(match_num[0]) # 자신이 낸 카드와 일치하는 바닥카드를 가져감
            player_get_card[player_turn].append(get_throw_card)
            player_get_card[player_turn].append(match_num2[0]) # 뒤집은 카드 + 일치하는 카드 3장을 모두 가져간다
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            player_get_card[player_turn].append(draw_card)            
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            rob_card(player_turn)# 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            remove_card_image("floor", match_num[0])
            remove_card_image("floor", draw_card)
            remove_card_image("floor", get_throw_card)
            remove_card_image("floor", match_num2[0])
            remove_card_image("floor", match_num2[1])
            remove_card_image("floor", match_num2[2])
            
    elif(match_count==2): # 바닥카드와 2개가 일치할 때 - 무덤카드를 뒤집어보고 같은 카드가 나오지 않으면 가져갈 카드 선택
                                                         #같은 카드가 나온 경우 모두 가져가고 각 플레이어들에게 피 1장씩 받음
        if(match_count2==0): # 뒤집은 카드와 일치하는 카드가 없을 때
            if(match_num[0] == match_num[1]): # 일치하는 바닥카드 2장이 같은 모양일 경우
                print("아무거나 가져옴(2,0)\n")
                player_get_card[player_turn].append(match_num[0]) # 낸 카드 + 일치하는 아무 카드 1장 가져간다
                player_get_card[player_turn].append(get_throw_card)                
                floor_card.append(draw_card) # 뒤집은 카드는 바닥에 놓음
                floor_card.remove(match_num[0])
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", get_throw_card)
            else: # 일치하는 바닥카드 2장이 다른 모양일 경우
                print("선택해서 가져옴(2,0)\n")
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(get_throw_card)  
                floor_card.append(draw_card)
                floor_card.remove(choice)
                remove_card_image("floor", choice)
                remove_card_image("floor", get_throw_card)
        elif(match_count2==1): # 뒤집은 카드와 일치하는 카드가 1장 일 때
            if(match_num[0] == match_num[1]):
                print("아무거나 가져옴(2,1)\n")
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num2[0])
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", get_throw_card)
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
            else:
                print("선택해서 가져옴(2,1)\n")
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)  
                floor_card.remove(choice)
                floor_card.remove(match_num2[0])
                remove_card_image("floor", choice)
                remove_card_image("floor", get_throw_card)
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
        elif(match_count2==2): # 뒤집은 카드와 일치하는 카드가 2장 일 때
            if(abs(get_throw_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 일치하는 경우(따닥)
                print("따닥!!\n")
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(match_num[1])
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num[0])
                floor_card.remove(match_num[1])
                rob_card(player_turn)#각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", match_num[1])
                remove_card_image("floor", get_throw_card)                
                remove_card_image("floor", draw_card)
            else: # 낸 카드와 뒤집은 카드가 일치하지 않는 경우(따닥이 아닌 경우)
                if(match_num[0] == match_num[1]):  # 같은 모양(1st)
                    if(match_num2[0] == match_num2[1]): # 같은 모양(2nd)
                        print("첫번째:아무거나, 두번째:아무거나(2,2)\n")
                        player_get_card[player_turn].append(match_num[0])
                        player_get_card[player_turn].append(get_throw_card)
                        player_get_card[player_turn].append(match_num2[0])
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(match_num[0])
                        floor_card.remove(match_num2[0])
                        remove_card_image("floor", match_num[0])
                        remove_card_image("floor", get_throw_card)
                        remove_card_image("floor", match_num2[0])                                        
                        remove_card_image("floor", draw_card)
                    else: # 다른 모양(2nd)
                        print("첫번째:아무거나, 두번째:선택(2,2)\n")
                        player_get_card[player_turn].append(match_num[0])
                        player_get_card[player_turn].append(get_throw_card)
                        choice = choice_card(match_num2[0], match_num2[1])
                        player_get_card[player_turn].append(choice)                       
                        player_get_card[player_turn].append(draw_card)  
                        floor_card.remove(choice)
                        floor_card.remove(match_num[0])
                        remove_card_image("floor", match_num[0])
                        remove_card_image("floor", get_throw_card)
                        remove_card_image("floor", choice)                                        
                        remove_card_image("floor", draw_card)
                else: # 다른 모양(1st)                    
                    if(match_num2[0] == match_num2[1]): # 같은 모양(2nd)
                        print("첫번째:선택, 두번째:아무거나(2,2)\n")
                        choice = choice_card(match_num[0], match_num[1])
                        player_get_card[player_turn].append(choice)
                        player_get_card[player_turn].append(get_throw_card)
                        player_get_card[player_turn].append(match_num2[0])
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(choice)
                        floor_card.remove(match_num2[0])
                        remove_card_image("floor", choice)
                        remove_card_image("floor", get_throw_card)
                        remove_card_image("floor", match_num2[0])                                        
                        remove_card_image("floor", draw_card)
                    else: # 다른 모양(2nd)
                        print("첫번째:선택, 두번째:선택(2,2)\n")
                        choice1 = choice_card(match_num[0], match_num[1])
                        player_get_card[player_turn].append(choice1)
                        player_get_card[player_turn].append(get_throw_card)
                        choice2 = choice_card(match_num2[0], match_num2[1])
                        player_get_card[player_turn].append(choice2)
                        player_get_card[player_turn].append(draw_card)
                        floor_card.remove(choice1)
                        floor_card.remove(choice2)
                        remove_card_image("floor", choice1)
                        remove_card_image("floor", get_throw_card)
                        remove_card_image("floor", choice2)                                        
                        remove_card_image("floor", draw_card)
                        
        elif(match_count2==3): # 뒤집은 카드와 일치하는 카드가 3장 일 때
            if(match_num[0] == match_num[1]):
                print("아무거나 가져온다 + 싼거먹음(2,3)\n")
                get_pee_wild_card(draw_card)
                player_get_card[player_turn].append(match_num[0])
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(match_num2[1])
                player_get_card[player_turn].append(match_num2[2])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                floor_card.remove(match_num2[1])
                floor_card.remove(match_num2[2])
                rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
                remove_card_image("floor", match_num[0])
                remove_card_image("floor", get_throw_card)
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", match_num2[1])
                remove_card_image("floor", match_num2[2])
                remove_card_image("floor", draw_card)
            else:
                print("선택해서 가져온다 + 싼거먹음(2,3)\n")
                get_pee_wild_card(draw_card)
                choice = choice_card(match_num[0], match_num[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(match_num2[1])
                player_get_card[player_turn].append(match_num2[2])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                floor_card.remove(match_num2[1])
                floor_card.remove(match_num2[2])
                floor_card.remove(choice)
                rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
                remove_card_image("floor", choice)
                remove_card_image("floor", get_throw_card)
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", match_num2[1])
                remove_card_image("floor", match_num2[2])
                remove_card_image("floor", draw_card)
                
    elif(match_count==3): # 바닥카드와 3개가 일치할 때 - 모두 가져가고 각 플레이어들에게 피 1장씩 받음
        print("싼거 먹음\n")
        get_pee_wild_card(get_throw_card)
        player_get_card[player_turn].append(get_throw_card)
        player_get_card[player_turn].append(match_num[0])
        player_get_card[player_turn].append(match_num[1])
        player_get_card[player_turn].append(match_num[2])
        floor_card.remove(match_num[0])
        floor_card.remove(match_num[1])
        floor_card.remove(match_num[2])
        rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
        remove_card_image("floor", get_throw_card)
        remove_card_image("floor", match_num[0])
        remove_card_image("floor", match_num[1])
        remove_card_image("floor", match_num[2])
        if(match_count2==0):
            print("(3,0)\n")
            floor_card.append(draw_card)
        elif(match_count2==1):
            print("(3,1)\n")
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(draw_card)
            floor_card.remove(match_num2[0])
            remove_card_image("floor", match_num2[0])
            remove_card_image("floor", draw_card)
        elif(match_count2==2):
            if(match_num2[0] == match_num2[1]):
                print("아무거나(3,2)\n")
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
            else:
                print("선택(3,2)\n")
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(choice)
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(choice)
                remove_card_image("floor", choice)
                remove_card_image("floor", draw_card)
        elif(match_count2==3):
            print("싼거 또 먹음(3,3)\n")
            get_pee_wild_card(draw_card)
            player_get_card[player_turn].append(draw_card)
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
            remove_card_image("floor", draw_card)
            remove_card_image("floor", match_num2[0])
            remove_card_image("floor", match_num2[1])
            remove_card_image("floor", match_num2[2])
    else: # 바닥카드와 일치하지 않을 때        
        if(match_count2==0):
            if(abs(get_throw_card - draw_card) < 4): # 낸 카드와 뒤집은 카드가 같은 경우(쪽)
                print("쪽\n")
                set_filename("kiss")
                threading._start_new_thread(play_sound,())
                player_get_card[player_turn].append(draw_card)
                player_get_card[player_turn].append(get_throw_card)
                rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)
                remove_card_image("floor", draw_card)
                remove_card_image("floor", get_throw_card)
            else:
                print("아무것도 못 먹음(0,0)\n")
                floor_card.append(get_throw_card)
                floor_card.append(draw_card)
        elif(match_count2==1):            
            print("(0,1)\n")
            floor_card.append(get_throw_card)
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(draw_card)
            floor_card.remove(match_num2[0])
            remove_card_image("floor", match_num2[0])
            remove_card_image("floor", draw_card)
        elif(match_count2==2):
            if(match_num2[0] == match_num2[1]):
                print("아무거나(0,2)\n")
                floor_card.append(get_throw_card)
                player_get_card[player_turn].append(match_num2[0])
                player_get_card[player_turn].append(draw_card)
                floor_card.remove(match_num2[0])
                remove_card_image("floor", match_num2[0])
                remove_card_image("floor", draw_card)
            else:
                print("선택(0,2)\n")
                floor_card.append(get_throw_card)
                choice = choice_card(match_num2[0], match_num2[1])
                player_get_card[player_turn].append(draw_card)
                player_get_card[player_turn].append(choice)
                floor_card.remove(choice)
                remove_card_image("floor", choice)
                remove_card_image("floor", draw_card)
        elif(match_count2==3):
            print("싼거 먹음(0,3)\n")
            get_pee_wild_card(draw_card)
            floor_card.append(get_throw_card)
            player_get_card[player_turn].append(draw_card)
            player_get_card[player_turn].append(match_num2[0])
            player_get_card[player_turn].append(match_num2[1])
            player_get_card[player_turn].append(match_num2[2])
            floor_card.remove(match_num2[0])
            floor_card.remove(match_num2[1])
            floor_card.remove(match_num2[2])
            rob_card(player_turn) # 각 플레이어에게 피카드 1장씩 가져온다(있을 경우에만)            
            remove_card_image("floor", draw_card)
            remove_card_image("floor", match_num2[0])
            remove_card_image("floor", match_num2[1])
            remove_card_image("floor", match_num2[2])
    for i in range(wild_card): # 뒤집어서 나온 와일드 카드를 모두 가져온다(싼 경우 제외)
        player_get_card[player_turn].append(13)
    if(len(floor_card)==0): #싹쓸
        print("싹쓸!")
        rob_card(player_turn)

#카드 2장 중 가져갈 카드를 선택해야 하는 경우
def choice_card(select1, select2):
    choice_list=[select1,select2]
    send_msg("choice",choice_list,player_turn)
    choice = int(recv_msg(player_turn))    
    return choice
#같은 종류 카드를 3장 가지고 있을 경우 흔들지 말지 결정
def choice_shake(player_num):
    is_shake = False
    send_msg("shake", 0, player_num)
    is_shake = int(recv_msg(player_num))    
    if(is_shake == 1):
        player_shake_count[player_num] += 1
        print("\n흔들었습니다!\n")

# 점수가 3점 이상일 때 GO/STOP 여부
def choice_go_stop(player_num):
    global player_prev_score, player_score
    
    send_msg("gostop", 0, player_num)
    select = int(recv_msg(player_num))

    if(select==1):
        print("      고!!\n")
        set_filename("go_1")
        threading._start_new_thread(play_sound,())
        player_go_count[player_num] += 1
        player_prev_score[player_num] = player_score[player_num]
    else:
        print("    스톱!!\n")
        set_filename("stop")
        threading._start_new_thread(play_sound,())
        game_over(player_num)
    
#와일드 카드와 함께 싼 경우 와일드 카드 처리 연산
def get_pee_wild_card(get_throw_card):
    global pee_card, pee_count, player_get_card, player_turn
    get_wild_count=0
    print(pee_card)
    print(len(pee_card))
    for i in range(len(pee_card)):
        if(pee_card[i][0]-get_throw_card < 4): #싼 카드와 같이 있는 와일드 카드 갯수를 구함
            get_wild_count = pee_card[i][1]
            print(get_wild_count)
            break            
    if(get_wild_count>=1):
        for i in range(get_wild_count): #와일드 카드 갯수만큼 획득            
            player_get_card[player_turn].append(13)
            floor_card.remove(13)
            remove_card_image("floor",13,loNum=int(get_throw_card/10))

#상대방의 피 1장 가져온다(있을 경우에만)
def rob_card(player_num):
    blood_list = [[17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117], [13, 116, 128]] #[[피],[쌍피]]
    for i in range(player):
        get_blood_count = 0 
        get_blood_card = 0
        if(i != player_num): #자신을 제외한 나머지 플레이어
            for j in range(len(player_get_card[i])): #피 카드 유무 검사
                get_blood_count = blood_list[0].count(player_get_card[i][j]) 
                if(get_blood_count>=1): #피 카드가 있을 경우
                    get_blood_card = player_get_card[i][j]
                    break
            if(get_blood_count==0): #피 카드가 없으면 쌍피 카드 검사
                for k in range(len(player_get_card[i])):
                    get_blood_count = blood_list[1].count(player_get_card[i][k]) 
                    if(get_blood_count>=1): #쌍피 카드가 있을 경우
                        get_blood_card = player_get_card[i][k]
                        break
            if(get_blood_count==0): #피 카드와 쌍피 카드가 둘다 없으면 가져오지 않음
                continue
            player_get_card[i].remove(get_blood_card) #상대방 패에서 삭제하고
            player_get_card[player_num].append(get_blood_card)# 내 패로 가져온다
            update_card_image(i, player_get_card[i])
    

#무덤카드 뒤집기
def draw_tombcard():
    global tomb_card
    tombcard=tomb_card[0]
    tomb_card.remove(tomb_card[0])
    print("\n카드를 뒤집었습니다: %d\n" % tombcard)
    return tombcard

#점수 계산
def calculate_score(player_num, september_state):
    global player_get_card, player_score, is_blood_card
    
    blood_list = [[17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117], [13, 116, 128]] #[[피],[쌍피]] - 10장부터 장당 1점
    band_list = [[16, 26, 36], [66, 96, 106], [46, 56, 76], [127]] #[[홍단],[청단],[초단],[띠]] - 홍단,청단,초단: 3점, 띠: 5장부터 장당 1점
    animal_list = [[25, 45, 86], [55, 65, 75, 105, 126]] #[[고도리],[동물]] - 고도리: 5점, 동물: 5장부터 장당 1점, 7개: 멍텅구리(점수x2)
    light_list = [[15, 35, 85, 115], [125]] #[[광],[비광]] - 3광: 3점(단, 비광포함 시 2점), 5광: 15점
    
    player_score[player_num]=0
    blood_count=0
    band_count=[0,0,0,0]
    animal_count=[0,0]
    light_count=[0,0]
    score_double=0

    isblood=False #피로 났는지 여부
    islight=False #광으로 났는지 여부
    
    if(september_state==1): #9월(95번)을 피로 처리
        blood_list[1].append(95)
    else: #9월(95번)을 동물로 처리
        animal_list[1].append(95)
       
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

    
        
    if((blood_count > 0) & (blood_count <= 5)): # 피가 1~5장 일 경우 피박
        player_oneself[player_num][0] = True
    else: # 피가 0장이거나 6장이상 일 경우 피박이 아님
        player_oneself[player_num][0] = False
    if(blood_count >= 10):
        isblood = True
        player_score[player_num] += blood_count-9 #피 점수
        print("      피: %d점 " % (blood_count-9))
        
    if(band_count[0] == 3):
        player_score[player_num] += 3 #홍단
        print("    홍단: 3점 ")
        set_filename("redlabel")
        threading._start_new_thread(play_sound,())
    if(band_count[1] == 3):
        player_score[player_num] += 3 #청단
        print("    청단: 3점 ")
        set_filename("bluelabel")
        threading._start_new_thread(play_sound,())
    if(band_count[2] == 3):
        player_score[player_num] += 3 #초단
        print("    초단: 3점 ")
        set_filename("grasslabel")
        threading._start_new_thread(play_sound,())
    band_sum = band_count[0] + band_count[1] + band_count[2]
    if(band_sum >= 5):
        player_score[player_num] +=  band_sum-4 #띠 점수
        print("      띠: %d점 " % (band_sum-4))
        
    light_sum = light_count[0] + light_count[1]
    if(light_sum == 0): # 광이 한 장도 없을 경우 광박
        player_oneself[player_num][1] = True
    else: # 광이 한 장 이상 있을 경우 광박 아님
        player_oneself[player_num][1] = False
    if(light_sum >=3 ):
        islight = True
    if(light_sum == 3): #3광
        if(light_count[1]==1): #비광 포함
            player_score[player_num] += 2
            print(" 3광(비): 2점 ")
            set_filename("light_three")
            threading._start_new_thread(play_sound,())
        else: #비광 비포함
            player_score[player_num] += 3
            print("     3광: 3점 ")
            set_filename("light_three")
            threading._start_new_thread(play_sound,())
    elif(light_sum == 4): #4광
        player_score[player_num] += 4
        print("     4광: 4점 ")
        set_filename("light_four")
        threading._start_new_thread(play_sound,())
    elif(light_sum == 5): #5광
        player_score[player_num] += 15
        print("     5광: 15점 ")
        set_filename("light_five")
        threading._start_new_thread(play_sound,())
    if(animal_count[0] == 3):
        player_score[player_num] += 5 #고도리
        print("  고도리: 5점 ")
        set_filename("godori")
        threading._start_new_thread(play_sound,())
    animal_sum = animal_count[0] + animal_count[1]
    if(animal_sum >= 5):
        player_score[player_num] +=  animal_sum-4 #동물 점수
        print("    동물: %d점 " % (animal_sum-4))
        if(animal_sum>=7):
            score_double += 1 #멍텅구리(점수x2배)
            print("멍텅구리: 2배 ")
    if(player_go_count[player_num]==1): #1고 - 1점
        player_score[player_num] += 1
        print("     1고: 1점 ")
        set_filename("go_1")
        threading._start_new_thread(play_sound,())
    elif(player_go_count[player_num]==2): #2고 - 2점
        player_score[player_num] += 2
        print("     2고: 2점 ")
        set_filename("go_2")
        threading._start_new_thread(play_sound,())
    elif(player_go_count[player_num]==3): #3고 - 2배
        score_double += 1
        print("     3고: 2배 ")
        set_filename("go_3")
        threading._start_new_thread(play_sound,())
    elif(player_go_count[player_num]==4): #4고 - 4배
        score_double += 2
        print("     4고: 4배 ")
    elif(player_go_count[player_num]==5): #5고 - 8배
        score_double += 3
        print("     5고: 8배 ")
        
    if(score_double != 0):
        player_score[player_num] *= pow(2,score_double)
    
    print("\n%d번 플레이어 점수 : %d점" % (player_num+1, player_score[player_num]))
    print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

    return isblood, islight    
            
#게임 종료(게임 결과 출력)
def game_over(player_num):
    isblood, islight = calculate_score(player_num, september_choice[player_num])
    for i in range(player):
        if(i != player_num): #승자 외 다른 플레이어가
            if(player_go_count[i] >=1): #고 상태일 경우
                print("%d번 플레이어는 고박입니다\n" % (i+1))
            if(player_shake_count[i] >=1): #흔든 상태일 경우
                print("%d번 플레이어는 흔들박입니다\n" % (i+1))
            if(isblood==True):
                if(player_oneself[i][0]==True):
                    print("%d번 플레이어는 피박입니다\n" % (i+1))
            if(islight==True):
                if(player_oneself[i][1]==True):
                    print("%d번 플레이어는 광박입니다\n" % (i+1))
    print("승자는 %d번 플레이어 입니다!\n" % (player_num+1))
    set_filename("winner")
    threading._start_new_thread(play_sound,())
    game_start()
    sys.exit()

threading._start_new_thread(init_gui,())
init_socket()
game_start()

