import socket
import threading
from PiSTOP_Client_GUI import *

#플레이어 손 카드
my_hand=[]

#선택 할 카드 리스트
choice_list=[]

HOST='192.168.219.109' #localhost
PORT=50007 #서버와 같은 포트사용
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
s.connect((HOST,PORT))

def send_msg(command,msg):
    msg = str(msg)
    msg = str(command+" "+msg)
    s.send(msg.encode('utf-8'))
    
def recv_msg():
    while 1:#command에 따른 작업
        r_data=0
        r_data=s.recv(1024) #서버로 부터 정보를 받음
        r_data = repr(r_data.decode('utf-8'))
        r_data = r_data.strip('\'')
        command,r_data = r_data.split(' ',1)
        if(command=="hand"):            
            global my_hand
            r_data = r_data.strip('\'[]')
            r_data = r_data.split(', ')
            my_hand=r_data            
            for i in range(len(my_hand)):
                my_hand[i] = int(my_hand[i])
            set_hand(my_hand)
            update_card()
        if(command=="turn"):
            set_turnFlag(True)
            set_turn_image()
            throw_card()
            print("throw")
        if(command=="choice"):
            global choice_list
            r_data = r_data.strip('\'[]')
            r_data = r_data.split(', ')
            choice_list = r_data
            choice_card()
        if(command=="shake"):
            choice_shake()
        if(command=="gostop"):
            choice_go_stop()
        if(command=="connect"):
            send_msg("connect", 1)
def throw_card():
    #낼 카드를 선택하고 카드를 낸다    
    while 1:
        n = get_throw_card()
        if(n!=0):          
            send_msg("throw", n)
            set_throw_card(0)
            set_turnFlag(False)
            set_turn_image()
            return

def choice_card():
    global choice_list
    select_card(int(choice_list[0]),int(choice_list[1]))
    while 1:
        if(get_select_index() != 0):
            send_msg("choice",choice_list[get_select_index()])

def choice_shake():
    while 1:
        if(get_answer_index() != 0):
            send_msg("shake", get_answer_index())

def choice_go_stop():
    while 1:
        if(get_gostop_index() != 0):
            send_msg("gostop", get_gostop_index())

threading._start_new_thread(recv_msg,())
threading._start_new_thread(init_gui,())
