import time
from tkinter import *

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

#GUI 초기화
def init_gui():
    global root, ws, hs, main_frame
    root = Tk() #최상위 위젯 생성
    root.title("PiSTOP - ACTION GOSTOP GAME") #타이틀 설정
    
    ws = root.winfo_screenwidth() #스크린 넓이
    hs = root.winfo_screenheight() #스크린 높이
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
    root.geometry('%dx%d+%d+%d' % (ws, hs, 0, -35))

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
    tombCard = Button(main_frame, bg='red', height=3, width=4, state=DISABLED).place(x=ws*0.46, y=hs*0.30)
    for j in range(len(floorcard_frame)):
        for i in range(5):
            floorCard = Label(floorcard_frame[j], bg=floor_color, text=str(j)+str(i))
            floorLabels[j][i] = floorCard            

#플레이어 획득 카드를 위한 프레임 생성
def create_getcard_frame():
    pc1_x=830
    pc1_y=630
    pc1_blood = Frame(main_frame, bg=floor_color)
    pc1_blood.pack(expand=1)
    pc1_blood.place(x=pc1_x, y=pc1_y-203)

    pc1_band = Frame(main_frame, bg=floor_color)
    pc1_band.pack(expand=1)
    pc1_band.place(x=pc1_x-180, y=pc1_y-50)

    pc1_animal = Frame(main_frame, bg=floor_color)
    pc1_animal.pack(expand=1)
    pc1_animal.place(x=pc1_x-360, y=pc1_y-50)
    
    pc1_light = Frame(main_frame, bg=floor_color)
    pc1_light.pack(expand=1)
    pc1_light.place(x=pc1_x-540, y=pc1_y)
    
    playercard_frame[0].append(pc1_blood)
    playercard_frame[0].append(pc1_band)
    playercard_frame[0].append(pc1_animal)
    playercard_frame[0].append(pc1_light)

    pc2_x=20
    pc2_y=580
    pc2_blood = Frame(main_frame, bg=floor_color)
    pc2_blood.pack(expand=1)
    pc2_blood.place(x=pc2_x, y=pc2_y-520)

    pc2_band = Frame(main_frame, bg=floor_color)
    pc2_band.pack(expand=1)
    pc2_band.place(x=pc2_x, y=pc2_y-240)

    pc2_animal = Frame(main_frame, bg=floor_color)
    pc2_animal.pack(expand=1)
    pc2_animal.place(x=pc2_x, y=pc2_y-120)
    
    pc2_light = Frame(main_frame, bg=floor_color)
    pc2_light.pack(expand=1)
    pc2_light.place(x=pc2_x, y=pc2_y)
    
    playercard_frame[1].append(pc2_blood)
    playercard_frame[1].append(pc2_band)
    playercard_frame[1].append(pc2_animal)
    playercard_frame[1].append(pc2_light)

    pc3_x=1075
    pc3_y=580
    pc3_blood = Frame(main_frame, bg=floor_color)
    pc3_blood.pack(expand=1)
    pc3_blood.place(x=pc3_x, y=pc3_y-520)

    pc3_band = Frame(main_frame, bg=floor_color)
    pc3_band.pack(expand=1)
    pc3_band.place(x=pc3_x, y=pc3_y-240)

    pc3_animal = Frame(main_frame, bg=floor_color)
    pc3_animal.pack(expand=1)
    pc3_animal.place(x=pc3_x, y=pc3_y-120)
    
    pc3_light = Frame(main_frame, bg=floor_color)
    pc3_light.pack(expand=1)
    pc3_light.place(x=pc3_x, y=pc3_y)
    
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
def update_card_image(player_num, player_card):
    blood_list = [17, 27, 37, 47, 57, 67, 77, 87, 97, 107, 117, 13, 116, 128]
    band_list = [16, 26, 36, 66, 96, 106, 46, 56, 76, 127]
    animal_list = [25, 45, 86, 55, 65, 75, 105, 126]
    light_list = [15, 35, 85, 115, 125]
    for i in range(3):
        playerBloodCards[player_num].clear()
        playerBandCards[player_num].clear()
        playerAnimalCards[player_num].clear()
        playerLightCards[player_num].clear()
    
    for i in player_card: #카드 분류
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
