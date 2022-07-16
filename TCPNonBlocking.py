from socket import *
import sys

serverName = '127.0.0.3'
serverPort = 1234
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:

    # client_message = sys.stdin.readline()
    # clientSocket.send(str.encode(client_message))
    response = clientSocket.recv(1024)
    print(response.decode('utf-8'))

