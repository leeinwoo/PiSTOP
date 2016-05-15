from tkinter import *

floor_color = '#50AF49' #바닥 배경색 RGB CODE
floorcard_frame = [] #바닥 카드 프레임
floorLabels = [[0 for i in range(5)] for i in range(12)] #바닥 카드 레이블
floorCards = [[] for i in range(12)] #바닥 카드 목록
image = [0 for i in range(130)] #로드 이미지
#카드 사이즈
card_height=45
card_width=27

#창 크기 설정
def set_window():
    root.geometry('%dx%d+%d+%d' % (ws, hs, ws*0.05,hs*0.05))

#바닥 카드를 위한 월별 프레임 생성
def create_floorcard_frame():
    baseX=40
    fc1 = Frame(main_frame)
    fc1.pack(expand=1)
    fc1.place(x=(ws/2-baseX-150), y=(hs/2-40-60))
    floorcard_frame.append(fc1)
    
    fc2 = Frame(main_frame)
    fc2.pack(expand=1)
    fc2.place(x=(ws/2-baseX-200), y=(hs/2-40))
    floorcard_frame.append(fc2)

    fc3 = Frame(main_frame)
    fc3.pack(expand=1)
    fc3.place(x=(ws/2-baseX-150), y=(hs/2-40+60))
    floorcard_frame.append(fc3)

    fc4 = Frame(main_frame)
    fc4.pack(expand=1)
    fc4.place(x=(ws/2-baseX+50), y=(hs/2-40-60))
    floorcard_frame.append(fc4)

    fc5 = Frame(main_frame)
    fc5.pack(expand=1)
    fc5.place(x=(ws/2-baseX+100), y=(hs/2-40))
    floorcard_frame.append(fc5)

    fc6 = Frame(main_frame)
    fc6.pack(expand=1)
    fc6.place(x=(ws/2-baseX+50), y=(hs/2-40+60))
    floorcard_frame.append(fc6)

    fc7 = Frame(main_frame)
    fc7.pack(expand=1)
    fc7.place(x=(ws/2-baseX-200), y=(hs/2-40-60-60))
    floorcard_frame.append(fc7)
    
    fc8 = Frame(main_frame)
    fc8.pack(expand=1)
    fc8.place(x=(ws/2-baseX-200), y=(hs/2-40+60+60))
    floorcard_frame.append(fc8)

    fc9 = Frame(main_frame)
    fc9.pack(expand=1)
    fc9.place(x=(ws/2-baseX+100), y=(hs/2-40-60-60))
    floorcard_frame.append(fc9)

    fc10 = Frame(main_frame)
    fc10.pack(expand=1)
    fc10.place(x=(ws/2-baseX+100), y=(hs/2-40+60+60))
    floorcard_frame.append(fc10)

    fc11 = Frame(main_frame)
    fc11.pack(expand=1)
    fc11.place(x=(ws/2-baseX-40), y=(hs/2-40-60-60-60))
    floorcard_frame.append(fc11)

    fc12 = Frame(main_frame)
    fc12.pack(expand=1)
    fc12.place(x=(ws/2-baseX-40), y=(hs/2-40+60+60+60))
    floorcard_frame.append(fc12)

#바닥카드 이미지 레이블 생성(프레임 당 최대 5개 - 쌌을때3장 + 와일드카드2장)
def create_image_label():
    global floorcard_frame, floorLabels
    tombCard = Button(main_frame, bg='red', height=3, width=4).place(x=(ws/2-80), y=(hs/2-40))
    for j in range(len(floorcard_frame)):
        for i in range(5):
            floorCard = Label(floorcard_frame[j], text=str(j)+str(i))
            floorLabels[j][i] = floorCard

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
def set_card_image(cardType, imageNum):
    if(cardType=="floor"): # 바닥 카드 깔기
        locateNum = int(imageNum/10)    
        l = len(floorCards[locateNum-1])
        floorCards[locateNum-1].append(imageNum)
        floorLabels[locateNum-1][l].config(image=image[imageNum], height=45, width=27)
        floorLabels[locateNum-1][l].grid(row=0, column=l)

#초기화 작업    
root = Tk()
root.title("PiSTOP - ACTION GOSTOP GAME")
ws = root.winfo_screenwidth()*0.7
hs = root.winfo_screenheight()*0.7
set_window()
main_frame = Frame(root, background=floor_color) #메인 프레임 생성(최상위 위젯에 붙임)
main_frame.pack(fill=BOTH, expand=1)

create_floorcard_frame()
create_image_label()
get_image()

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
print(floorCards)

root.mainloop()
