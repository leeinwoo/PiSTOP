import socket, threading, time

HOST=''
PORT=50007 #프로세스 포트
socket_list=[] #소켓 리스트
client=0 #클라이언트 수 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #소켓 속성
delay=0.1 #send 시 약간의 딜레이를 줌

#서버 소켓 초기화, 접속 쓰레드 실행
def init_socket():        
    s.bind((HOST,PORT))
    s.listen(3)
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
    for i in range(3):
        send_msg("connect", 0, i)
        is_connect = recv_msg(i)
        if(is_connect==False):
            socket_list[i].close()
            socket_list.pop(i)
            client -= 1

#클라이언트 수
def get_client():
    return client
