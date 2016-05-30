import time
from tkinter import *

root=0
ws=0
hs=0
main_frame=0
card_frame=0
select_frame=0

cardLabels=[0 for i in range(7)] # 손 카드 이미지 레이블
selectLabels=[0 for i in range(3)] # 선택 카드 이미지 레이블

bg_color = '#50AF49' #배경색 RGB CODE

image = [0 for i in range(130)] #로드 이미지

#GUI 초기화
def init_gui():
    global root, ws, hs, main_frame
    root = Tk() #최상위 위젯 생성
    root.title("PiSTOP - ACTION GOSTOP GAME") #타이틀 설정
    
    ws = root.winfo_screenwidth()*0.3 #스크린 넓이
    hs = root.winfo_screenheight()*0.4 #스크린 높이
    set_window() #윈도우 창 크기 설정
    
    main_frame = Frame(root, background=bg_color) #메인 프레임 생성(최상위 위젯에 붙임)
    main_frame.pack(fill=BOTH, expand=1) #출력
    
    create_frame()
    create_label()
    
    get_image()

    #root.mainloop()

#창 크기 설정
def set_window():
    root.geometry('%dx%d+%d+%d' % (340, 240, 0, 0))

#카드 프레임 생성
def create_frame():
    global card_frame, select_frame
    card_frame = Frame(main_frame, bg=bg_color)
    card_frame.pack(expand=1)

    select_frame = Frame(main_frame, bg=bg_color)
    select_frame.pack(expand=1)

#카드 이미지 레이블 생성
def create_label():
    for i in range(7):
        my_card = Label(card_frame, bg=bg_color)
        cardLabels[i] = my_card
        cardLabels[i].grid(row=4-int(i/4), column=i%4)
    for i in range(3):
        select_card = Label(select_frame, bg=bg_color)
        selectLabels[i] = select_card
        selectLabels[i].grid(row=0, column=i)

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

#카드 이미지 갱신
def update_card(card_list):
    print(len(card_list))
    for i in range(7):
        cardLabels[i].grid_forget()
        my_card = Label(card_frame, bg=bg_color)
        cardLabels[i] = my_card
        cardLabels[i].grid(row=4-int(i/4), column=i%4)
    for i in range(len(card_list)):
        cardLabels[i].config(image=image[card_list[i]])
        cardLabels[i].grid(row=4-int(i/4), column=i%4)

#전체 이미지 삭제
def clear():
    for i in range(7):
        cardLabels[i].grid_forget()
    for i in range(3):
        selectLabels[i].grid_forget()

#카드 선택
def select_card(select1, select2, select3=0):
    selectLabels[0].config(image=image[select1])
    selectLabels[0].grid(row=0, column=0)

    selectLabels[1].config(image=image[select2])
    selectLabels[1].grid(row=0, column=1)

    if(select3!=0):
        selectLabels[2].config(image=image[select3])
        selectLabels[2].grid(row=0, column=2)

# yes, no 선택
def select_answer(select):
    if(select==1):
        selectLabel = Label(main_frame, bg=bg_color, text="click")
        selectLabel.pack(expand=1)
        selectLabel.bind("<Button-1>",onclick)

def onclick(event):
    print("onclick")

init_gui()
card=[15, 17, 27, 37, 47, 125, 126]
update_card(card)
clear()
select_card(15,17)
clear()
select_answer(1)
root.mainloop()
