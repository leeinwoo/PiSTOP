import socket
import threading
import time

HOST='127.0.0.1'
PORT=50007
socket_list=[]
client=0
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
def connect():
    global s, client
    while 1:        
        conn, addr=s.accept() #접속 승인
        socket_list.append(conn)
        threading._start_new_thread(recv_msg,(conn,client))
        threading._start_new_thread(send_msg,(conn,client))
        client+=1
        print('conn:', socket_list)
        print('Connected by',addr)
        print('socket name:',s.getsockname())
def send_msg(conn,num):
    while 1:
        time.sleep(1)
        socket_list[num].send(str(num).encode('utf-8'))
def recv_msg(conn,num):
    while 1:
        data=conn.recv(1024)
        print(num,data)
   
threading._start_new_thread(connect,())
while 1:
    pass
"""while True:

    data=conn.recv(1024)

    if not data: break

    conn.send(data) #받은 데이터를 그대로 클라이언트에 전송

conn.close()
"""
