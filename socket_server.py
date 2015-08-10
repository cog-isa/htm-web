import shutil
import socket
import os
import threading
from htm_server import htm_server

def start_htm_server(port):
    s=htm_server(port)
    s.start()


def main():
    SOCKET_PORT = 10100

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', SOCKET_PORT)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        data = ""
        data += connection.recv(512).decode('utf-8')
        connection.close()
        print(data)
        if data.find('runServer:') != -1:
            port = int(data[len('runServer:'):])
            print(port)
            thread = threading.Thread(target=start_htm_server, args=(port,))
            thread.daemon = True
            thread.start()



    # thread = threading.Thread(target=start_java_socket_server, args=())
    # thread.daemon = True
    # thread.start()

main()

