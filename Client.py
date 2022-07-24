import _thread
from random import randint
from time import sleep
from socket import *
from tqdm import tqdm
import sys

class Connection:
    def __init__(self, serverName, serverPort) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        # self.clientSocket.bind(('127.0.0.1', 5001))
        # self.clientSocket.listen(5)
        self.clientSocket.connect((serverName, serverPort))

ipGenerator = f'127.0.0.{randint(5,100)}'

print(ipGenerator)

def server(serverName, port):
    serverPort = 5001
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((ipGenerator, serverPort))
    serverSocket.listen(5)

    while True:
        connectionSocket, addr = serverSocket.accept()

        msg = connectionSocket.recv(1024).decode('utf-8')

        connectionSocket.send(f'pica->{msg}'.encode())


def downloadFile(type, ip, file):
    downloadServer = socket(AF_INET, SOCK_STREAM)
    downloadServer.connect((ip, 5001))

    downloadServer.send(f'{type};{ip};{file}'.encode())

    callback = downloadServer.recv(1024).decode('utf-8')
    print(callback)

    for i in tqdm(range(int(9e6))):
        pass

    return 


if len(sys.argv) < 2:
    raise Exception("Informe IP arq1.txt")

# Porta fixa 1234 do Server de pares
conn = Connection(sys.argv[1], 1234)

messageToSend = ipGenerator + ';' + ';'.join(sys.argv[2::])
conn.clientSocket.send(f'{messageToSend}'.encode())

_thread.start_new_thread(server, conn.clientSocket.getsockname())

while True:
    client_message = sys.stdin.readline()

    match client_message.split():
        case ["get", _, _]:
            downloadFile(*client_message.split(), )
            conn.clientSocket.send(str.encode("abuble"))
        case ["exit"]:
            conn.clientSocket.send(str.encode(client_message))
            sys.exit()
        case _:
            conn.clientSocket.send(str.encode(client_message))

    response = conn.clientSocket.recv(1024)
    print(response.decode('utf-8'))
