import _thread
import sys
import os
from random import randint
from time import sleep
from socket import *
from tqdm import tqdm
from Peer import Peer


# Simular os endereços
ipGenerator = f'127.0.0.{randint(5,100)}'

# Hr que for rodar entre pcs mesmo
# ipGenerator = gethostbyname(gethostname())

print(ipGenerator)

def server(serverName, port):
    serverPort = 5001
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((ipGenerator, serverPort))
    serverSocket.listen(5)

    while True:
        connectionSocket, addr = serverSocket.accept()
        _thread.start_new_thread(on_new_peer_transfer, (connectionSocket, addr))
       

def on_new_peer_transfer(peerSocket, addr):
    msg = peerSocket.recv(1024).decode('utf-8')

    peerSocket.send(f'::DEBUG:: {msg}'.encode())

    match msg.split():
        case ['get', _]:
            _, fileName = msg.split()
            os.path.abspath(fileName)
            Peer.sendFile(conn=peerSocket, file_name=fileName, addr=addr)

        

def downloadFile(type, ip, file):
    downloadSocket = socket(AF_INET, SOCK_STREAM)
    downloadSocket.connect((ip, 5001))

    downloadSocket.send(f'{type};{ip};{file}'.encode())

    data = downloadSocket.recv(1024)

    f = open('file', 'wb')
    while data != bytes(''.encode()):
        #print(data)
        data = downloadSocket.recv(1024)
        f.write(data)

    print(f':: Arquivo {file} em mãos')
    

if len(sys.argv) < 3:
    raise Exception("Informe IP arq1.txt")

# Porta fixa 1234 do Server de pares

try:
    conn = Peer(sys.argv[1], 1234)
except Exception:
    sys.exit()

messageToSend = ipGenerator + ';' + ';'.join(sys.argv[2::])
conn.clientSocket.send(f'{messageToSend}'.encode())

_thread.start_new_thread(server, conn.clientSocket.getsockname())

while True:
    client_message = sys.stdin.readline()

    match client_message.split():
        case ["get", _, _]:
            downloadFile(*client_message.split(), )
            conn.clientSocket.send(str.encode("get sucesses"))
        case ["exit"]:
            conn.clientSocket.send(str.encode(client_message))
            sys.exit()
        case _:
            conn.clientSocket.send(str.encode(client_message))

    response = conn.clientSocket.recv(1024)
    print(response.decode('utf-8'))
