#-*- coding: cp949 -*-
import time, threading
from tkinter import *
from mpu6050 import *

root=0
ws=0
hs=0

cardLabels=[0 for i in range(7)] # �� ī�� �̹��� ���̺�
selectLabels=[0 for i in range(3)] # ���� ī�� �̹��� ���̺�
answerLabels=[0 for i in range(3)] # answer question image label
gostopLabels=[0 for i in range(3)] # gostop question image label

bg_color = '#50AF49' #���� RGB CODE

image = [0 for i in range(150)] #�ε� �̹���
card=[]
tmp_throw_card=0
throw_card=0
my_turn=False
select_index=0

#GUI �ʱ�ȭ
def init_gui():
    global root, ws, hs, main_frame
    root = Tk() #�ֻ��� ���� ����
    root.title("PiSTOP - ACTION GOSTOP GAME") #Ÿ��Ʋ ����
    
    ws = root.winfo_screenwidth() #��ũ�� ����
    hs = root.winfo_screenheight() #��ũ�� ����
    set_window() #������ â ũ�� ����
    
    main_frame = Frame(root, background=bg_color) #���� ������ ����(�ֻ��� ������ ����)
    main_frame.pack(fill=BOTH, expand=1) #���
    
    create_frame()
    create_label()
    
    get_image()

    root.mainloop()

#â ũ�� ����
def set_window():
    root.geometry('%dx%d+%d+%d' % (ws/2, hs/2, 0, 0))

#ī�� ������ ����
def create_frame():
    global card_frame, select_frame, throw_frame, answer_frame, gostop_frame
    card_frame = Frame(main_frame, bg=bg_color)
    card_frame.pack(expand=1, fill=BOTH)

    select_frame = Frame(main_frame, bg=bg_color)
    select_frame.pack(expand=1, fill=BOTH)

    throw_frame = Frame(main_frame, bg=bg_color)    
    throw_frame.pack(expand=1, fill=BOTH)

    answer_frame = Frame(main_frame, bg=bg_color)
    answer_frame.pack(expand=1, fill=BOTH)

    gostop_frame = Frame(main_frame, bg=bg_color)
    gostop_frame.pack(expand=1, fill=BOTH)

#ī�� �̹��� ���̺� ����
def create_label():
    for i in range(7):
        my_card = Label(card_frame, bg=bg_color)
        cardLabels[i] = my_card
        cardLabels[i].grid(row=4-int(i/4), column=i%4)        

    for i in range(3):
        select_card = Label(select_frame, bg=bg_color)
        selectLabels[i] = select_card
        selectLabels[i].grid(row=0, column=i)

    for i in range(3):
        answer_q = Label(answer_frame, bg=bg_color)
        answerLabels[i] = answer_q
        answerLabels[i].pack()

    for i in range(2):
        gostop_q = Label(gostop_frame, bg=bg_color)
        gostopLabels[i] = gostop_q
        gostopLabels[i].pack()

    global throwLabel
    throwLabel = Label(throw_frame, bg=bg_color)

#ī�� �̹��� �ε�
def get_image():
    image_count=0
    for num in range(len(image)):
        try:
            image[num] = PhotoImage(file="./res/"+str(num)+".png")
            image_count += 1            
        except :            
            continue
    image[149] = PhotoImage(file="./res/shake.png")
    image[148] = PhotoImage(file="./res/yes.png")
    image[147] = PhotoImage(file="./res/no.png")
    for num in range(147,150):
        image[num] = image[num].subsample(3, 3)
    image[146] = PhotoImage(file="./res/go.png")
    image[145] = PhotoImage(file="./res/stop.png")
    for num in range(145,147):
        image[num] = image[num].subsample(2, 2)
    
    image_count += 5
        #image[num] = image[num].subsample(2,2)
    print("%d���� �̹����� �ε��߽��ϴ�." % image_count)

#card image zoom
def zoom_image(multi):    
    for num in range(len(image)):
        try:
            image[num] = image[num].zoom(multi, multi)
        except:
            continue
        
#card image subsample
def subsample_image(sub):
    for num in range(len(image)):
        try:
            image[num] = image[num].subsample(sub, sub)
        except:
            continue
    
#ī�� �̹��� ����
def update_card():    
    global card
    clear()
    card_frame.place(x=100,y=40)
    for i in range(len(card)):
        cardLabels[i].config(image=image[card[i]])
        cardLabels[i].grid(row=4-int(i/4), column=i%4)
        cardLabels[i].bind("<Button-1>",onclick_hand)

#��ü �̹��� ����
def clear():
    global throwLabel
    for i in range(7):
        cardLabels[i].grid_forget()
    for i in range(3):
        selectLabels[i].grid_forget()
    for i in range(3):
        answerLabels[i].pack_forget()
    for i in range(2):
        gostopLabels[i].pack_forget()
    throwLabel.pack_forget()
    
    card_frame.place(x=1000,y=1000)
    select_frame.place(x=1000,y=1000)
    throw_frame.place(x=1000,y=1000)
    answer_frame.place(x=1000,y=1000)
    gostop_frame.place(x=1000,y=1000)

#ī�� ����
def select_card(select1, select2):
    clear()
    zoom_image(2)
    select_frame.place(x=150,y=100)
    selectLabels[0].config(image=image[select1])
    selectLabels[0].grid(row=0, column=0)
    selectLabels[0].bind("<Button-1>", onclick_select)

    selectLabels[1].config(image=image[select2])
    selectLabels[1].grid(row=0, column=1)
    selectLabels[1].bind("<Button-1>", onclick_select)

# yes, no ����
def select_answer():
    clear()
    answer_frame.place(x=70,y=50)
    answerLabels[0].config(image=image[149])
    answerLabels[0].pack()

    answerLabels[1].config(image=image[148])
    answerLabels[1].pack()
    answerLabels[1].bind("<Button-1>", onclick_answer)

    answerLabels[2].config(image=image[147])
    answerLabels[2].pack()
    answerLabels[2].bind("<Button-1>", onclick_answer)

#go, stop ����
def select_gostop():
    clear()
    gostop_frame.place(x=130,y=40)
    gostopLabels[0].config(image=image[146])
    gostopLabels[0].pack()
    gostopLabels[0].bind("<Button-1>", onclick_gostop)

    gostopLabels[1].config(image=image[145])
    gostopLabels[1].pack()
    gostopLabels[1].bind("<Button-1>", onclick_gostop)

#click handcard event
def onclick_hand(event):
    global card, tmp_throw_card
    if(my_turn==True):
        for i in range(len(card)):
            if(event.widget==cardLabels[i]):
                print("clickcard")
                zoom_image(2)
                tmp_throw_card=card[i]
                get_throw_cardImg(tmp_throw_card)            
                get_value()
                threading._start_new_thread(get_decide, ())

#click selectcard event
def onclick_select(event):
    global selectLabels
    if(my_turn==True):
        for i in range(len(selectLabels)):
            if(event.widget==selectLabels[i]):
                set_select_index(i)

def onclick_answer(event):
    global answerLabels
    if(my_turn==True):
        for i in range(len(answerLabels)):
            if(event.widget==answerLabels[i]):
                set_answer_index(i)

def onclick_gostop(event):
    global gostopLabels
    if(my_turn==True):
        for i in range(len(gostopLabels)):
            if(event.widget==gostopLabels[i]):
                set_gostop_index(i)     

def get_decide():
    global card, throw_card
    while 1:
        if(is_decide() == True):
            subsample_image(2)
            clear()
            set_decide(False)            
            set_throw_card(tmp_throw_card)            
            break
        
def set_hand(my_hand):
    global card
    card = my_hand

def set_turnFlag(flag):
    global my_turn    
    my_turn = flag

def set_throw_card(n):
    global throw_card
    throw_card = n

def get_throw_card():
    global throw_card
    return throw_card

def set_select_index(n):
    global select_index
    select_index = n

def get_select_index():
    global select_index
    return int(select_index)

def set_answer_index(n):
    global answer_index
    answer_index = n

def get_answer_index():
    global answer_index
    return int(answer_index)

def set_gostop_index(n):
    global gostop_index
    gostop_index = n

def get_gostop_index():
    global gostop_index
    return int(gostop_index)

#get throw card
def get_throw_cardImg(card):
    global throwLabel
    clear()
    throwLabel.config(image=image[card])
    throw_frame.place(x=180,y=50)
    throwLabel.pack(expand=1, fill=BOTH)

"""
init_gui()
card=[15,15,15,15,15,15,15]
update_card()
clear()
zoom_image(2)
get_throw_cardImg(15)
subsample_image(2)
clear()
update_card()
clear()
select_gostop()
clear()
select_answer()

root.mainloop()

"""
