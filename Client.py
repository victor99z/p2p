import _thread
import sys
import os
from random import randint
from socket import *
from Peer import Peer


if len(sys.argv) < 3:
    raise Exception("Informe IP arq1.txt")

# Porta fixa 1234 do Server de pares

try:
    conn = Peer(sys.argv[1], 1234)
except Exception:
    sys.exit()


# Simular os endereços dentro da msm maquina
ipGenerator = f'127.0.0.{randint(5,100)}'

# IP interno caso use em outros PC's 
#ipGenerator = conn.clientSocket.getsockname()[0]

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

    match msg.split(";"):
        case ['get', _]:
            _, fileName = msg.split(";")
            filename_full = os.path.abspath(fileName)

            if (os.path.exists(filename_full)):
                Peer.sendFile(conn=peerSocket, file_name=filename_full, addr=addr)
            else:
                peerSocket.send("error arquivo nao existe".encode())


def downloadFile(type, ip, file):
    downloadSocket = socket(AF_INET, SOCK_STREAM)
    downloadSocket.connect((ip, 5001))

    downloadSocket.send(f'{type};{file}'.encode())

    data = downloadSocket.recv(1024)

    match data.split():
        case ["error"]:
            print("Arquivo inexistente!")
            conn.clientSocket.send(str.encode('exit'))
            sys.exit()
        case _:
            file = str(randint(0,100)) + file
    
            f = open(file, 'wb')
            while data != bytes(''.encode()):
                data = downloadSocket.recv(1024)
                f.write(data)

            print(f':: Arquivo {file} em mãos')
    

messageToSend = ipGenerator + ';' + ';'.join(sys.argv[2::])
conn.clientSocket.send(f'{messageToSend}'.encode())

_thread.start_new_thread(server, conn.clientSocket.getsockname())

while True:
    client_message = sys.stdin.readline()

    match client_message.split():
        case ["get", _, _]:
            tipo, ip, filename = client_message.split()
            downloadFile(tipo, ip, filename)
            conn.clientSocket.send(str.encode(f'add {ipGenerator} {filename}'))
        case ["exit"]:
            conn.clientSocket.send(str.encode(client_message))
            sys.exit()
        case _:
            conn.clientSocket.send(str.encode(client_message))

    response = conn.clientSocket.recv(1024)
    print(response.decode('utf-8'))
