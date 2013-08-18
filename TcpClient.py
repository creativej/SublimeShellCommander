
import socket

class TcpClient:
    def __init__(self, host, port):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((host, port))
        self.sendIndex = []

    def send(self, command):
        print('sending...')
        self.session.send(command.encode('utf-8'))
        data = self.session.recv(1024)
        self.close()
        return data

    def close(self):
        self.session.close()
