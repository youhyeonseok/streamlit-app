import socket

# 서버 IP와 포트 설정
HOST = '192.168.80.104'  # 서버 IP를 지정
PORT = 80            # 서버와 동일한 포트 번호

# 소켓 생성 및 서버 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 서버에 메시지 전송
try:
    message = "스맥".encode('utf-8')
    client_socket.sendall(message)
    client_socket.settimeout(300)  # 10초 타임아웃 설정
    data = client_socket.recv(1024)
    print("서버로부터 받은 응답:", data.decode('utf-8'))
finally:
    client_socket.close()  # 소켓 종료

