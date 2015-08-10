import shutil
import socket
import os
import threading
import pickle
from htm_server import htm_server
from socketModule import socketModule


def start_htm_server(port):
    s=htm_server(port)
    s.start()

def handle(data):
    data=data.decode('utf-8')
    print(data)
    if data.find('runServer:') != -1:
            port = int(data[len('runServer:'):])
            print(port)
            thread = threading.Thread(target=start_htm_server, args=(port,))
            thread.daemon = True
            thread.start()
            return {"status":200}
    else:
        return {"status":404}

def main():
    SOCKET_PORT = 10100
    server=socketModule()
    server.openLocalPort(SOCKET_PORT)

    while True:
        server.waitForRqst(handle)


    # thread = threading.Thread(target=start_java_socket_server, args=())
    # thread.daemon = True
    # thread.start()

main()

