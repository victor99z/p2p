from socket import *
import sys

# Servidor que armazena os pares
serverName = '127.0.0.3'
serverPort = 1234
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send(str.encode(str(sys.argv[0])))
clientSocket.send()

while True:
    client_message = sys.stdin.readline()
    clientSocket.send(str.encode(client_message))
    response = clientSocket.recv(1024)
    print(int(response))

