from socket import *
from tqdm import tqdm

class Peer:
    def __init__(self, serverName, serverPort) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

    @staticmethod
    def sendFile(file_name, conn, addr):
        # progress = tqdm.tqdm(range(size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            conn.send(data)
            while len(data) > 0:
                data = file.read(1024)
                conn.send(data)
                
            # progress.update(1024)

