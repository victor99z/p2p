from socket import *

class Peer:
    def __init__(self, serverName, serverPort) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

    @staticmethod
    def sendFile(file_name, conn, addr):
        
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            conn.send(data)
            while data != bytes(''.encode()):
                data = file.read(1024)
                conn.send(data)
            
        conn.close()
