import socket

Host='localhost' 

Port=12345

socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((Host, Port))

socket.send("Hello we re connected".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))
