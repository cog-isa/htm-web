import socket as _socket


class SocketServer:
    def __init__(self, port):
        self.port = str(port)
        self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.server_address = ('localhost', int(self.port))
        self.socket.bind(self.server_address)
        self.socket.listen(1)
        self.end_message = "[END_MESSAGE]"
        self.connection = None

    def send_message(self, message):
        self.connection.sendall(bytes(str(message) + self.end_message, 'UTF-8'))

    def receive_message(self):
        self.connection, client_address = self.socket.accept()

        res = ""
        while True:
            q = self.connection.recv(1024).decode('utf-8')
            res += q
            if res.find(self.end_message) != -1:
                break

        return res.replace(self.end_message, "")

    def close(self):
        self.socket.close()


class SocketClient:
    # Клиент написан так, что всегда ждет ответа от сокета
    # TODO добавить время ожидания ответа

    def __init__(self, port):
        self.port = port
        self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)

        self.end_message = "[END_MESSAGE]"

    def request(self, message):
        self.socket.connect(('localhost', self.port))
        self.socket.sendall(bytes(str(message) + self.end_message, 'UTF-8'))

        res = ""
        while True:
            q = self.socket.recv(1024).decode('utf-8')
            res += q
            if res.find(self.end_message) != -1:
                break

        return res.replace(self.end_message, "")

    def close(self):
        self.socket.close()
