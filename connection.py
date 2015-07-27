import socket
import os
import sys


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


def turn_on_java_machine(socket_port):
    SERVER_SOCKET_PORT = 10100
    host = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, SERVER_SOCKET_PORT))
        sock.sendall(bytes("runServer:%s\n" % socket_port, 'UTF-8'))
    except ConnectionRefusedError:
        pass
    finally:
        sock.close()


def stop_java_server(socket_port):
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
    host = "localhost"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"

    try:
        sock.connect((host, socket_port))
        sock.sendall(bytes("get" + "\n", 'UTF-8'))

        data = ""

        while data.find(end_message) == -1:
            data += sock.recv(1024).decode('utf-8')
        data = data.replace(end_message, "")
    except ConnectionRefusedError:
        data = "{'data':'0'}"
    finally:
        sock.close()

    return data


if __name__ == '__main__':
    pass