import jsonpickle

__author__ = 'gmdidro'
import pickle
import socket

class socketModule:

    def close(self):
        self.sock.close()

    def openLocalPort(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        self.sock.bind(server_address)
        self.sock.listen(1)



    def waitForRqst(self, handle):
        connection, client_address = self.sock.accept()
        data = bytes()
        data += connection.recv(512)
        answer=jsonpickle.encode(handle(data))

        end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"
        connection.sendall(bytes(answer, 'UTF-8'))
        connection.sendall(bytes(end_message, 'UTF-8'))
        connection.close()

    def sendRqst(self,hostname, port, cmd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, port))

        self.sock.sendall(cmd)
        end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"

        data = ""

        while True:
            try:
                q = self.sock.recv(1024).decode('utf-8')
                data = data + q
                if q.find(end_message) != -1:
                    break
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
                pass

        end_start=data.find(end_message)
        data=data[:end_start]

        self.sock.close()
        # obj = jsonpickle.decode(data)
        return data