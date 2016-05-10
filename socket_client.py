import socket
import threading
HOST='127.0.0.1' #localhost
PORT=50007 #서버와 같은 포트사용
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓생성
s.connect((HOST,PORT))
def send_msg():
    while 1:
        s_data = input()
        s.send(s_data.encode('utf-8')) #문자를 보냄
def recv_msg():
    while 1:
        r_data=0
        r_data=s.recv(1024) #서버로 부터 정보를 받음
        print('Received',repr(r_data.decode('utf-8')))

threading._start_new_thread(send_msg,())
#threading._start_new_thread(recv_msg,())

#s.close()
