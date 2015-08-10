import socket
import os
import sys
from socketModule import socketModule


def do_connect(port):
    host = "localhost"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sock.sendall(bytes("get\n", 'UTF-8'))
    data = sock.recv(1024)
    sock.sendall(bytes("close\n", 'UTF-8'))

    sock.close()
    return data


def test_connect(socket_port):
    host = "localhost"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, socket_port))
        sock.sendall(bytes("close\n", 'UTF-8'))
        sock.close()
        return True
    except ConnectionRefusedError:
        sock.close()
        return False


def turn_on_htm_server(socket_port):
    SOCKET_SERVER_PORT = 10100
    host = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, SOCKET_SERVER_PORT))
        sock.sendall(bytes("runServer:%s\n" % socket_port, 'UTF-8'))
    except ConnectionRefusedError:
        pass
    finally:
        sock.close()


def stop_htm_server(socket_port):
    host = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, socket_port))
        sock.sendall(bytes("exit\n", 'UTF-8'))
    except ConnectionRefusedError:
        sock.close()
        return False
    return True


def send(socket_port, data):
    host = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, socket_port))
    sock.sendall(bytes(data + "\n", 'UTF-8'))
    sock.close()


def receive(socket_port):
    client=socketModule()
    obj=client.sendRqst("localhost",socket_port,bytes("get:", 'UTF-8'))

    return obj


if __name__ == '__main__':
    pass