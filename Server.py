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

    ip, arquivos = clientsocket.recv(1024).decode('utf-8').split(';')
    pares[ip] = arquivos

    while True:
        message = clientsocket.recv(1024)
        message = message.decode('utf-8')

        if not message:
            break

        match message.split():
            case ['peers']:
                total_peers = ", ".join(list(pares.keys()))
                clientsocket.send(str.encode(f"-> Seus vizinhos são: {total_peers}\n"))
            case ['ls', _]:
                ip_arquivos = message.split()[1]
                clientsocket.send(str.encode("-> Arquivos: " + json.dumps(pares[ip_arquivos], indent=1)))
            case ['exit']:
                pares.pop(ip)
                clientsocket.close()
                sys.exit()
            case ['rm', _, _]:
                # TODO: pqp fudeu
                pass
            case _:
                clientsocket.send(
                    str.encode("-> Comando inválido \n-> (peers, ls [ip], get [ip] [arquivo.txt]), exit"))


while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'Bem vindo {addr}')
    _thread.start_new_thread(on_new_client, (connectionSocket, addr))

