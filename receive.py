import socket
import sys

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',60666))
serversocket.listen(1)

while True:
    (clientsocket, address) = serversocket.accept()
    sockin = clientsocket.makefile()
    while True:
        data = sockin.read(1024)
        if data=='':
            break
        print len(data)
