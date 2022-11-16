import socket

TCP_IP = '192.168.56.1'
TCP_PORT = 27015
BUFFER_SIZE = 1024
MESSAGE = "Fuck!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(MESSAGE)
#data = s.recv(BUFFER_SIZE)
s.close()

#print ("send data:", data)