import random, sys, socket, threading, time
from tkinter import *


# # # # # 소켓 통신 전역 변수 # # # # #
HOST='127.0.0.1'
PORT=50007 #프로세스 포트
socket_list=[] #소켓 리스트
client=0 #클라이언트 수 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #소켓 속성
delay=0.01 #send 시 약간의 딜레이를 줌
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # GUI 전역 변수 # # # # # # # # # #
#초기화 변수
root=0
ws=0
hs=0
main_frame=0

floor_color = '#50AF49' #바닥 배경색 RGB CODE
floorcard_frame = [] #바닥 카드 프레임
floorLabels = [[0 for i in range(5)] for i in range(12)] #바닥 카드 레이블
floorCards = [[] for i in range(12)] #바닥 카드 목록

playercard_frame = [[] for i in range(3)] #플레이어 카드 프레임
playerBloodLabels = [[0 for i in range(25)] for i in range(3)] #플레이어 피 카드 레이블
playerBandLabels = [[0 for i in range(10)] for i in range(3)] #플레이어 띠 카드 레이블
playerAnimalLabels = [[0 for i in range(9)] for i in range(3)] #플레이어 동물 카드 레이블
playerLightLabels = [[0 for i in range(5)] for i in range(3)] #플레이어 광 카드 레이블
playerBloodCards = [[] for i in range(3)] #플레이어 피 카드 목록
playerBandCards = [[] for i in range(3)] #플레이어 띠 카드 목록
playerAnimalCards = [[] for i in range(3)] #플레이어 동물 카드 목록
playerLightCards = [[] for i in range(3)] #플레이어 광 카드 목록

image = [0 for i in range(130)] #로드 이미지

#카드 사이즈
card_height=45
card_width=27
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # GAME 전역 변수 # # # # # # # # # #
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # 소켓 통신 함수 # # # # # # # # # # 
#서버 소켓 초기화, 접속 쓰레드 실행
def init_socket():        
    s.bind((HOST,PORT))
    s.listen(5)
    threading._start_new_thread(connect,())
    
#클라이언트 접속대기 및 연결, 데이터 통신 쓰레드 실행
def connect():
    global s, client
    while 1:
        if(client>=3):
            break
        conn, addr=s.accept() #접속 승인
        socket_list.append(conn)
        client+=1        
        print(addr,'님이 접속하셨습니다')
        
#클라이언트에게 메세지 보냄
def send_msg(command,msg,num):
    msg = str(msg)
    msg = str(command+" "+msg)
    socket_list[num].send(msg.encode('utf-8'))
    time.sleep(delay)
    
#클라이언트로부터 메세지 받음
def recv_msg(num):
    data=0
    data=socket_list[num].recv(1024)
    data = repr(data.decode('utf-8'))
    data = data.strip('\'')
    command,data = data.split(' ',1)
    if(command=="throw"):
        return data
    if(command=="choice"):
        return data
    if(command=="shake"):
        return data
    if(command=="gostop"):
        return data
    if(command=="connect"):
        return data

#클라이언트 연결 상태 확인
def is_connect():
    for i in range(player):
        send_msg("connect", 0, i)
        is_connect = recv_msg(i)
        if(is_connect==False):
            socket_list[i].close()
            socket_list.pop(i)
            client -= 1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # GUI 함수 # # # # # # # # # #
#GUI 초기화
def init_gui():
    global root, ws, hs, main_frame
    root = Tk() #최상위 위젯 생성
    root.title("PiSTOP - ACTION GOSTOP GAME") #타이틀 설정
    
    ws = root.winfo_screenwidth()*0.7 #스크린 넓이
    hs = root.winfo_screenheight()*0.8 #스크린 높이
    set_window() #윈도우 창 크기 설정
    
    main_frame = Frame(root, background=floor_color) #메인 프레임 생성(최상위 위젯에 붙임)
    main_frame.pack(fill=BOTH, expand=1) #출력
    
    create_floorcard_frame()
    create_floor_image_label()

    create_getcard_frame()
    create_player_image_label()
    
    get_image()

    root.mainloop()
    
#창 크기 설정
def set_window():
    root.geometry('%dx%d+%d+%d' % (ws, hs, ws*0.05,hs*0.05))

#바닥 카드를 위한 월별 프레임 생성
def create_floorcard_frame():
    
    fc1 = Frame(main_frame, bg=floor_color)
    fc1.pack(expand=1)
    fc1.place(x=ws*0.37, y=hs*0.22)
    floorcard_frame.append(fc1)
    
    fc2 = Frame(main_frame, bg=floor_color)
    fc2.pack(expand=1)
    fc2.place(x=ws*0.34, y=hs*0.30)
    floorcard_frame.append(fc2)

    fc3 = Frame(main_frame, bg=floor_color)
    fc3.pack(expand=1)
    fc3.place(x=ws*0.37, y=hs*0.38)
    floorcard_frame.append(fc3)

    fc4 = Frame(main_frame, bg=floor_color)
    fc4.pack(expand=1)
    fc4.place(x=ws*0.52, y=hs*0.22)
    floorcard_frame.append(fc4)

    fc5 = Frame(main_frame, bg=floor_color)
    fc5.pack(expand=1)
    fc5.place(x=ws*0.55, y=hs*0.30)
    floorcard_frame.append(fc5)

    fc6 = Frame(main_frame, bg=floor_color)
    fc6.pack(expand=1)
    fc6.place(x=ws*0.52, y=hs*0.38)
    floorcard_frame.append(fc6)

    fc7 = Frame(main_frame, bg=floor_color)
    fc7.pack(expand=1)
    fc7.place(x=ws*0.34, y=hs*0.14)
    floorcard_frame.append(fc7)
    
    fc8 = Frame(main_frame, bg=floor_color)
    fc8.pack(expand=1)
    fc8.place(x=ws*0.34, y=hs*0.46)
    floorcard_frame.append(fc8)

    fc9 = Frame(main_frame, bg=floor_color)
    fc9.pack(expand=1)
    fc9.place(x=ws*0.55, y=hs*0.14)
    floorcard_frame.append(fc9)

    fc10 = Frame(main_frame, bg=floor_color)
    fc10.pack(expand=1)
    fc10.place(x=ws*0.55, y=hs*0.46)
    floorcard_frame.append(fc10)

    fc11 = Frame(main_frame, bg=floor_color)
    fc11.pack(expand=1)
    fc11.place(x=ws*0.46, y=hs*0.06)
    floorcard_frame.append(fc11)

    fc12 = Frame(main_frame, bg=floor_color)
    fc12.pack(expand=1)
    fc12.place(x=ws*0.46, y=hs*0.54)
    floorcard_frame.append(fc12)

#바닥카드 이미지 레이블 생성(프레임 당 최대 5개 - 쌌을때3장 + 와일드카드2장)
def create_floor_image_label():
    global floorcard_frame, floorLabels
    tombCard = Button(main_frame, bg='red', height=3, width=4).place(x=ws*0.46, y=hs*0.30)
    for j in range(len(floorcard_frame)):
        for i in range(5):
            floorCard = Label(floorcard_frame[j], bg=floor_color, text=str(j)+str(i))
            floorLabels[j][i] = floorCard            

#플레이어 획득 카드를 위한 프레임 생성
def create_getcard_frame():
    pc1_blood = Frame(main_frame, bg=floor_color)
    pc1_blood.pack(expand=1)
    pc1_blood.place(x=ws*0.62, y=hs*0.71)

    pc1_band = Frame(main_frame, bg=floor_color)
    pc1_band.pack(expand=1)
    pc1_band.place(x=ws*0.47, y=hs*0.88)

    pc1_animal = Frame(main_frame, bg=floor_color)
    pc1_animal.pack(expand=1)
    pc1_animal.place(x=ws*0.32, y=hs*0.88)
    
    pc1_light = Frame(main_frame, bg=floor_color)
    pc1_light.pack(expand=1)
    pc1_light.place(x=ws*0.17, y=hs*0.938)
    
    playercard_frame[0].append(pc1_blood)
    playercard_frame[0].append(pc1_band)
    playercard_frame[0].append(pc1_animal)
    playercard_frame[0].append(pc1_light)

    pc2_blood = Frame(main_frame, bg=floor_color)
    pc2_blood.pack(expand=1)
    pc2_blood.place(x=ws*0.01, y=hs*0.55)

    pc2_band = Frame(main_frame, bg=floor_color)
    pc2_band.pack(expand=1)
    pc2_band.place(x=ws*0.01, y=hs*0.40)

    pc2_animal = Frame(main_frame, bg=floor_color)
    pc2_animal.pack(expand=1)
    pc2_animal.place(x=ws*0.01, y=hs*0.25)
    
    pc2_light = Frame(main_frame, bg=floor_color)
    pc2_light.pack(expand=1)
    pc2_light.place(x=ws*0.01, y=hs*0.10)
    
    playercard_frame[1].append(pc2_blood)
    playercard_frame[1].append(pc2_band)
    playercard_frame[1].append(pc2_animal)
    playercard_frame[1].append(pc2_light)

    pc3_blood = Frame(main_frame, bg=floor_color)
    pc3_blood.pack(expand=1)
    pc3_blood.place(x=ws*0.87, y=hs*0.05)

    pc3_band = Frame(main_frame, bg=floor_color)
    pc3_band.pack(expand=1)
    pc3_band.place(x=ws*0.87, y=hs*0.38)

    pc3_animal = Frame(main_frame, bg=floor_color)
    pc3_animal.pack(expand=1)
    pc3_animal.place(x=ws*0.87, y=hs*0.55)
    
    pc3_light = Frame(main_frame, bg=floor_color)
    pc3_light.pack(expand=1)
    pc3_light.place(x=ws*0.87, y=hs*0.75)
    
    playercard_frame[2].append(pc3_blood)
    playercard_frame[2].append(pc3_band)
    playercard_frame[2].append(pc3_animal)
    playercard_frame[2].append(pc3_light)

#플레이어 획득 카드 이미지 레이블 생성
def create_player_image_label():
    global playercard_frame, playerBloodLabels, playerBandLabels, playerAnimalLabels, playerLightLabels
    for j in range(3): #피 카드 레이블 생성
        for i in range(25):
            playerCard = Label(playercard_frame[j][0], text="피", bg=floor_color, height=3, width=4)
            playerBloodLabels[j][i] = playerCard
            playerBloodLabels[j][i].grid(row=5-int(i/5), column=i%5)
    for j in range(3): #띠 카드 레이블 생성
        for i in range(10):
            playerCard = Label(playercard_frame[j][1], text="띠", bg=floor_color, height=3, width=4)
            playerBandLabels[j][i] = playerCard
            playerBandLabels[j][i].grid(row=5-int(i/5), column=i%5)
    for j in range(3): #동물 카드 레이블 생성
        for i in range(9):
            playerCard = Label(playercard_frame[j][2], text="동물", bg=floor_color, height=3, width=4)
            playerAnimalLabels[j][i] = playerCard
            playerAnimalLabels[j][i].grid(row=5-int(i/5), column=i%5)
    for j in range(3): #광 카드 레이블 생성
        for i in range(5):
            playerCard = Label(playercard_frame[j][3], text="광", bg=floor_color, height=3, width=4)
            playerLightLabels[j][i] = playerCard
            playerLightLabels[j][i].grid(row=0, column=i)

#카드 이미지 로드
def get_image():
    image_count=0
    for num in range(len(image)):
        try:
            image[num] = PhotoImage(file="./res/"+str(num)+".png")
            image_count += 1            
        except :            
            continue            
        image[num] = image[num].subsample(2,2)
    print("%d개의 이미지를 로드했습니다." % image_count)

#카드 이미지 출력
def set_card_image(cardType, imageNum, player_num=0, loNum=0):
    if(cardType=="floor"): # 바닥 카드 깔기
        if(imageNum==13): #와일드 카드
            locateNum = loNum
        else:
            locateNum = int(imageNum/10)
        l = len(floorCards[locateNum-1])
        floorCards[locateNum-1].append([imageNum, l])
        floorLabels[locateNum-1][l].config(image=image[imageNum], height=45, width=27)
        floorLabels[locateNum-1][l].grid(row=0, column=l)
    # 플레이어 획득 카드 깔기
    elif(cardType=="blood"):        
        l = len(playerBloodCards[player_num])
        playerBloodCards[player_num].append(imageNum)
        playerBloodLabels[player_num][l].config(image=image[imageNum], height=45, width=27)
        playerBloodLabels[player_num][l].grid(row=5-int(l/5), column=l%5)
    elif(cardType=="band"):
        l = len(playerBandCards[player_num])
        playerBandCards[player_num].append(imageNum)
        playerBandLabels[player_num][l].config(image=image[imageNum], height=45, width=27)
        playerBandLabels[player_num][l].grid(row=5-int(l/5), column=l%5)
    elif(cardType=="animal"):
        l = len(playerAnimalCards[player_num])
        playerAnimalCards[player_num].append(imageNum)
        playerAnimalLabels[player_num][l].config(image=image[imageNum], height=45, width=27)
        playerAnimalLabels[player_num][l].grid(row=5-int(l/5), column=l%5)
    elif(cardType=="light"):
        l = len(playerLightCards[player_num])
        playerLightCards[player_num].append(imageNum)
        playerLightLabels[player_num][l].config(image=image[imageNum], height=45, width=27)
        playerLightLabels[player_num][l].grid(row=0, column=l)
    time.sleep(0.5)

#카드 이미지 삭제
def remove_card_image(cardType, imageNum, player_num=0, loNum=0):
        if(cardType=="floor"): # 바닥 카드 지우기
            if(imageNum==13): #와일드 카드
                locateNum = loNum
            else:
                locateNum = int(imageNum/10)
            for i in range(len(floorCards[locateNum-1])):
                if(floorCards[locateNum-1][i][0]==imageNum):
                    index = floorCards[locateNum-1][i][1]
                    floorCards[locateNum-1].remove([imageNum,index])                    
                    floorLabels[locateNum-1][index].grid_forget()
                    break
        elif(cardType=="player"): # 플레이어 피 카드 지우기
            playerBloodCards[player_num].remove(imageNum)
            for i in range(25):
                playerBloodLabels[player_num][i].grid_forget()
                playerCard = Label(playercard_frame[player_num][0], text="피", bg=floor_color, height=3, width=4)
                playerBloodLabels[player_num][i] = playerCard
                playerBloodLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
            for i in range(len(playerBloodCards[player_num])):
                playerBloodLabels[player_num][i].config(image=image[playerBloodCards[player_num][i]], height=45, width=27)
                playerBloodLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
        time.sleep(0.5)

#플레이어 획득 카드 갱신
def update_card_image(player_num):
    blood_list = [17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117, 13, 116, 128]
    band_list = [16, 26, 36, 66, 96, 106, 46, 56, 76, 127]
    animal_list = [25, 45, 86, 55, 65, 75, 105, 126]
    light_list = [15, 35, 85, 115, 125]
    for i in range(player):
        playerBloodCards[player_num].clear()
        playerBandCards[player_num].clear()
        playerAnimalCards[player_num].clear()
        playerLightCards[player_num].clear()
        
    for i in player_get_card[player_num]: #카드 분류
        if(blood_list.count(i) > 0): #피
            playerBloodCards[player_num].append(i)        
        elif(band_list.count(i) > 0): #띠
            playerBandCards[player_num].append(i)
        elif(animal_list.count(i) > 0): #동물
            playerAnimalCards[player_num].append(i)
        elif(light_list.count(i) > 0): #광
            playerLightCards[player_num].append(i)
    #피 카드 갱신
    for i in range(25):
        playerBloodLabels[player_num][i].grid_forget()
        playerCard = Label(playercard_frame[player_num][0], text="피", bg=floor_color, height=3, width=4)
        playerBloodLabels[player_num][i] = playerCard
        playerBloodLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    for i in range(len(playerBloodCards[player_num])):
        playerBloodLabels[player_num][i].config(image=image[playerBloodCards[player_num][i]], height=45, width=27)
        playerBloodLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    #띠 카드 갱신
    for i in range(10):
        playerBandLabels[player_num][i].grid_forget()
        playerCard = Label(playercard_frame[player_num][1], text="띠", bg=floor_color, height=3, width=4)
        playerBandLabels[player_num][i] = playerCard
        playerBandLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    for i in range(len(playerBandCards[player_num])):
        playerBandLabels[player_num][i].config(image=image[playerBandCards[player_num][i]], height=45, width=27)
        playerBandLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    #동물 카드 갱신
    for i in range(9):
        playerAnimalLabels[player_num][i].grid_forget()
        playerCard = Label(playercard_frame[player_num][2], text="동물", bg=floor_color, height=3, width=4)
        playerAnimalLabels[player_num][i] = playerCard
        playerAnimalLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    for i in range(len(playerAnimalCards[player_num])):
        playerAnimalLabels[player_num][i].config(image=image[playerAnimalCards[player_num][i]], height=45, width=27)
        playerAnimalLabels[player_num][i].grid(row=5-int(i/5), column=i%5)
    #광 카드 갱신
    for i in range(5):
        playerLightLabels[player_num][i].grid_forget()
        playerCard = Label(playercard_frame[player_num][3], text="광", bg=floor_color, height=3, width=4)
        playerLightLabels[player_num][i] = playerCard
        playerLightLabels[player_num][i].grid(row=0, column=i)
    for i in range(len(playerLightCards[player_num])):
        playerLightLabels[player_num][i].config(image=image[playerLightCards[player_num][i]], height=45, width=27)
        playerLightLabels[player_num][i].grid(row=0, column=i)
    
#화면 초기화
def reset_gui():
    global floorCards, playerBloodCards, playerBandCards, playerAnimalCards, playerLightCards
    
    for i in range(3):        
        for j in range(25):
            playerBloodLabels[i][j].grid_remove()
        for j in range(10):
            playerBandLabels[i][j].grid_remove()
        for j in range(9):
            playerAnimalLabels[i][j].grid_remove()
        for j in range(5):
            playerLightLabels[i][j].grid_remove()
    for j in range(len(floorcard_frame)):
        for i in range(5):
            floorLabels[j][i].grid_remove()
    floorCards.clear()
    playerBloodCards.clear()
    playerBandCards.clear()
    playerAnimalCards.clear()
    playerLightCards.clear()

    floorCards = [[] for i in range(12)]
    playerBloodCards = [[] for i in range(3)]
    playerBandCards = [[] for i in range(3)]
    playerAnimalCards = [[] for i in range(3)]
    playerLightCards = [[] for i in range(3)]
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # GAME 함수 # # # # # # # # # # 
#게임 초기화 작업
def init():
    global player, player_turn, card
    card = [15, 16, 17, 17, 25, 26, 27, 27, 35, 36, 37, 37, 45, 46, 47, 47,
        55, 56, 57, 57, 65, 66, 67, 67, 75, 76, 77, 77, 85, 86, 87, 87,
        95, 96, 97, 97, 105, 106, 107, 107, 115, 116, 117, 117, 125, 126, 127, 128,
        13, 13]
    player = 3
    player_turn = 0
    while 1:
        if(client==3):# 3명이 접속하면 게임을 시작함
            time.sleep(0.5)
            print("게임이 곧 시작됩니다!\n")
            reset_gui()
            time.sleep(3)
            card_shuffle()
            card_share()
            update_card_image(0)
            update_card_image(1)
            update_card_image(2)
            break

#게임 시작
def game_start():    
    init()    
    global player_turn
    for i in range(7*player):
        is_connect()
        print("바닥 카드 : %s\n" % floor_card)
        print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
        throw_card()
        update_card_image(player_turn)
        card_sort()
        calculate_score(player_turn, september_choice[player_turn])
        if(player_score[player_turn] >= 3): # 플레이어 점수가 3점 이상이면
            if(player_go_count[player_turn] >= 1): # 고 상태일 경우(이전 점수랑 비교해서 1점이상 획득해야 고/스톱 가능)
                if(player_score[player_turn] - player_prev_score[player_turn] >= 1):
                    choice_go_stop(player_turn) # 고/스톱 여부 결정
            else: # 고 상태가 아닐 경우
                choice_go_stop(player_turn) # 고/스톱 여부 결정
        player_turn += 1
        if(player_turn>=player):
            player_turn=0
#카드 섞기
def card_shuffle():
    global card
    random.shuffle(card)
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
        update_card_image(player_turn)
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
        player_go_count[player_num] += 1
        player_prev_score[player_num] = player_score[player_num]
    else:
        print("    스톱!!\n")
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
            remove_card_image("player", get_blood_card, i)
            update_card_image(i)
    

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
    if(band_count[1] == 3):
        player_score[player_num] += 3 #청단
        print("    청단: 3점 ")
    if(band_count[2] == 3):
        player_score[player_num] += 3 #초단
        print("    초단: 3점 ")
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
        else: #비광 비포함
            player_score[player_num] += 3
            print("     3광: 3점 ")
    elif(light_sum == 4): #4광
        player_score[player_num] += 4
        print("     4광: 4점 ")
    elif(light_sum == 5): #5광
        player_score[player_num] += 15
        print("     5광: 15점 ")
    if(animal_count[0] == 3):
        player_score[player_num] += 5 #고도리
        print("  고도리: 5점 ")
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
    elif(player_go_count[player_num]==2): #2고 - 2점
        player_score[player_num] += 2
        print("     2고: 2점 ")
    elif(player_go_count[player_num]==3): #3고 - 2배
        score_double += 1
        print("     3고: 2배 ")
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
    game_start()
    sys.exit()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
threading._start_new_thread(init_gui,())
init_socket()
game_start()

