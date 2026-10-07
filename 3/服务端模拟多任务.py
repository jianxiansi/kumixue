import socket

serve_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serve_socket.bind(('192.168.***.***',10086))

serve_socket.listen(5)

while True:
    try:
        accept_socket,client_info = serve_socket.accept()

        accept_socket.send(b'nihao')

        data = accept_socket.recv(1024).decode('utf-8')

        print(f'服务端收到来自{client_info}的信息：{data}')

        accept_socket.close()
    except:
        pass