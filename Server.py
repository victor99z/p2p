import _thread
import sys
from socket import *

thread_count = 0
serverPort = 1234
pares = {}
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.3', serverPort))
serverSocket.listen(5)
print("SERVER READY")


def on_new_client(clientsocket, addr):
    clientsocket.send(str.encode('Welcome to the Server!\n'))

    while True:
        message = clientsocket.recv(1024)
        message = message.decode('utf-8')

        if not message:
            break

        match message.split():
            case ['peers']:
                clientsocket.send(str.encode("Seus vizinhos são: " + str(pares)))
            case ['ls']:
                clientsocket.send(str.encode("Os arquivos de [IP] são: [arq.txt, arq2.txt]"))
            case ['get']:
                # Como enviar o arquivo? descobriremos em breve
                pass
            case ['exit']:
                clientsocket.close()
                sys.exit()
            case _:
                clientsocket.send(
                    str.encode("Informe um dos seguintes comandos\n(ls [ip], get [ip] [arquivo.txt], peers)"))


while True:
    connectionSocket, addr = serverSocket.accept()
    _thread.start_new_thread(on_new_client, (connectionSocket, addr))
    thread_count += 1
    print(f'Threads: {thread_count}, conectado a {addr}')

connectionSocket.close()
