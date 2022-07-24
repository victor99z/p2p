
from socket import *
import sys


class Connection:
    def __init__(self, serverName, serverPort) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        # self.clientSocket.bind(('127.0.0.1', 5001))
        # self.clientSocket.listen(5)
        self.clientSocket.connect((serverName, serverPort))


if len(sys.argv) < 2:
    raise Exception("Informe IP arq1.txt")
else:
    conn = Connection(sys.argv[1], 1234)
    junta_nome_arquivos = ';'.join(sys.argv[1::])
    conn.clientSocket.send(f"{junta_nome_arquivos}".encode())

while True:
    client_message = sys.stdin.readline()

    match client_message.split():
        case ["get"]:
            print("yikes get arquivo")
        case ["exit"]:
            conn.clientSocket.send(str.encode(client_message))
            conn.clientSocket.close()
            sys.exit()
        case _:
            conn.clientSocket.send(str.encode(client_message))

    response = conn.clientSocket.recv(1024)
    print(response.decode('utf-8'))
