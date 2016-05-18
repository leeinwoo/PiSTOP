import socket
import threading

#플레이어 손 카드
my_hand=[]

#플레이어 순서
my_turn=0

#선택 할 카드 리스트
choice_list=[]

HOST='127.0.0.1' #localhost
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
        if(command=="turn"):
            my_turn = int(r_data)
            throw_card()
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
    global my_hand
    print(my_hand,"\n")
    print("내 차례입니다!\n")
    select = int(input('낼 카드의 index>> '))
    send_msg("throw",my_hand[select])

def choice_card():
    global choice_list
    print(choice_list)
    choice = int(input('가져올 카드의 index>> '))
    send_msg("choice",choice_list[choice])

def choice_shake():
    choice = int(input('흔드시겠습니까? 예(1), 아니오(0)>> '))
    send_msg("shake",choice)

def choice_go_stop():
    choice = int(input('GO/STOP 여부를 결정하세요 - GO(1), STOP(0)>>'))
    send_msg("gostop",choice)

#threading._start_new_thread(send_msg,())
threading._start_new_thread(recv_msg,())

#s.close()
