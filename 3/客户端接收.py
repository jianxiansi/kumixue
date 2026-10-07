import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('192.168.***.***',10086))

data = client.recv(1024).decode('utf-8')

print(data)

client.send(b'wohao')

client.close()
