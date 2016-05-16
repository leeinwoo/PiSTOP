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

#창 크기 설정
def set_window():
    root.geometry('%dx%d+%d+%d' % (ws, hs, ws*0.05,hs*0.05))

#바닥 카드를 위한 월별 프레임 생성
def create_floorcard_frame():
    
    fc1 = Frame(main_frame)
    fc1.pack(expand=1)
    fc1.place(x=ws*0.37, y=hs*0.22)
    floorcard_frame.append(fc1)
    
    fc2 = Frame(main_frame)
    fc2.pack(expand=1)
    fc2.place(x=ws*0.34, y=hs*0.30)
    floorcard_frame.append(fc2)

    fc3 = Frame(main_frame)
    fc3.pack(expand=1)
    fc3.place(x=ws*0.37, y=hs*0.38)
    floorcard_frame.append(fc3)

    fc4 = Frame(main_frame)
    fc4.pack(expand=1)
    fc4.place(x=ws*0.52, y=hs*0.22)
    floorcard_frame.append(fc4)

    fc5 = Frame(main_frame)
    fc5.pack(expand=1)
    fc5.place(x=ws*0.55, y=hs*0.30)
    floorcard_frame.append(fc5)

    fc6 = Frame(main_frame)
    fc6.pack(expand=1)
    fc6.place(x=ws*0.52, y=hs*0.38)
    floorcard_frame.append(fc6)

    fc7 = Frame(main_frame)
    fc7.pack(expand=1)
    fc7.place(x=ws*0.34, y=hs*0.14)
    floorcard_frame.append(fc7)
    
    fc8 = Frame(main_frame)
    fc8.pack(expand=1)
    fc8.place(x=ws*0.34, y=hs*0.46)
    floorcard_frame.append(fc8)

    fc9 = Frame(main_frame)
    fc9.pack(expand=1)
    fc9.place(x=ws*0.55, y=hs*0.14)
    floorcard_frame.append(fc9)

    fc10 = Frame(main_frame)
    fc10.pack(expand=1)
    fc10.place(x=ws*0.55, y=hs*0.46)
    floorcard_frame.append(fc10)

    fc11 = Frame(main_frame)
    fc11.pack(expand=1)
    fc11.place(x=ws*0.46, y=hs*0.06)
    floorcard_frame.append(fc11)

    fc12 = Frame(main_frame)
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
def set_card_image(cardType, imageNum, player_num=0):
    if(cardType=="floor"): # 바닥 카드 깔기
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

#카드 이미지 삭제
def remove_card_image(cardType, imageNum, player_num=0):
        if(cardType=="floor"): # 바닥 카드 지우기
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

def init():
    global root, ws, hs, main_frame
    root = Tk()
    root.title("PiSTOP - ACTION GOSTOP GAME")
    ws = root.winfo_screenwidth()*0.7
    hs = root.winfo_screenheight()*0.8
    set_window()
    main_frame = Frame(root, background=floor_color) #메인 프레임 생성(최상위 위젯에 붙임)
    main_frame.pack(fill=BOTH, expand=1)
    create_floorcard_frame()
    create_floor_image_label()

    create_getcard_frame()
    create_player_image_label()
    get_image()
            
#초기화 작업    
init()


a=[17,15]
temp_card = a.pop()
#test code
set_card_image("floor",temp_card)
set_card_image("floor",15)
set_card_image("floor",17)
set_card_image("floor",27)
set_card_image("floor",37)
set_card_image("floor",47)
set_card_image("floor",57)
set_card_image("floor",67)
set_card_image("floor",77)
set_card_image("floor",87)
set_card_image("floor",87)
set_card_image("floor",97)
set_card_image("floor",107)
set_card_image("floor",117)
set_card_image("floor",127)

for i in range(21):
    set_card_image("blood",17, 0)
    set_card_image("blood",17, 1)
    set_card_image("blood",17, 2)
for i in range(8):
    set_card_image("band",26, 0)
    set_card_image("band",26, 1)
    set_card_image("band",26, 2)
for i in range(6):
    set_card_image("animal",45, 0)
    set_card_image("animal",45, 1)
    set_card_image("animal",45, 2)
for i in range(4):
    set_card_image("light",35, 0)
    set_card_image("light",35, 1)
    set_card_image("light",35, 2)

remove_card_image("floor", 15)

remove_card_image("player", 17, 0)
remove_card_image("player", 17, 0)
set_card_image("blood",27, 0)
set_card_image("blood",47, 0)
set_card_image("blood",57, 0)
remove_card_image("player", 17, 0)
remove_card_image("player", 47, 0)

reset_gui()

#test code
set_card_image("floor",17)
set_card_image("floor",15)
set_card_image("floor",17)
set_card_image("floor",27)
set_card_image("floor",37)
set_card_image("floor",47)
set_card_image("floor",57)
set_card_image("floor",67)
set_card_image("floor",77)
set_card_image("floor",87)
set_card_image("floor",87)
set_card_image("floor",97)
set_card_image("floor",107)
set_card_image("floor",117)
set_card_image("floor",127)

for i in range(21):
    set_card_image("blood",17, 0)
    set_card_image("blood",17, 1)
    set_card_image("blood",17, 2)
for i in range(8):
    set_card_image("band",26, 0)
    set_card_image("band",26, 1)
    set_card_image("band",26, 2)
for i in range(6):
    set_card_image("animal",45, 0)
    set_card_image("animal",45, 1)
    set_card_image("animal",45, 2)
for i in range(4):
    set_card_image("light",35, 0)
    set_card_image("light",35, 1)
    set_card_image("light",35, 2)

remove_card_image("floor", 15)

remove_card_image("player", 17, 0)
remove_card_image("player", 17, 0)
set_card_image("blood",27, 0)
set_card_image("blood",47, 0)
set_card_image("blood",57, 0)
set_card_image("blood",13, 0)
remove_card_image("player", 17, 0)
remove_card_image("player", 47, 0)


root.mainloop()
