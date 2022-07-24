import json
import _thread
import sys
from socket import *

serverPort = 1234
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.3', serverPort))
serverSocket.listen(5)
pares = {}
print("SERVER READY")


def on_new_client(clientsocket, addr):

    arquivos = clientsocket.recv(1024).decode('utf-8').split(';')
    pares[addr[0]] = arquivos
    clientsocket.send(str.encode(f'Bem vindo {addr[0]}'))

    while True:
        message = clientsocket.recv(1024)
        message = message.decode('utf-8')

        if not message:
            break

        match message.split():
            case ['peers']:
                totalPeers = ",".join(list(pares.keys()))
                clientsocket.send(str.encode(f"Seus vizinhos são: {totalPeers}\n"))
            case ['ls']:
                ipArquivos = message.split()[1]
                clientsocket.send(str.encode("Arquivos: \n" + json.dumps(pares[ipArquivos], indent=1)))
            case ['exit']:
                pares.pop(addr[0])
                clientsocket.close()
                sys.exit()
            case _:
                clientsocket.send(
                    str.encode("Informe um dos seguintes comandos\n(peers, ls [ip], get [ip] [arquivo.txt])"))


while True:
    connectionSocket, addr = serverSocket.accept()
    _thread.start_new_thread(on_new_client, (connectionSocket, addr))
    print(f'Conectado a {addr}')

