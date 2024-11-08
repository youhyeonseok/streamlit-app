import socket

# 서버 IP와 포트 설정
HOST = '192.168.80.104'  # 서버 IP를 지정
PORT = 8000            # 서버와 동일한 포트 번호

# 소켓 생성 및 서버 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 서버에 메시지 전송
try:
    message = "파이썬으로 Hello 출력하는 방법".encode('utf-8')
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    print("서버로부터 받은 응답:", data.decode('utf-8'))
finally:
    client_socket.close()  # 소켓 종료
