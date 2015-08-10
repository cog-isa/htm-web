import socket
import os
import sys
from socketModule import socketModule


# def do_connect(socket_port):
#     client=socketModule()
#
#     obj=client.sendRqst("localhost",socket_port,bytes("get", 'UTF-8'))
#     obj=client.sendRqst("localhost",socket_port,bytes("close", 'UTF-8'))
#
#     return obj


# def test_connect(socket_port):
#     client=socketModule()
#     try:
#         obj=client.sendRqst("localhost",socket_port,bytes("close", 'UTF-8'))
#         return True
#     except ConnectionRefusedError:
#         client.close()
#         return False


def turn_on_htm_server(socket_port):
    SOCKET_SERVER_PORT = 10100
    client=socketModule()
    try:
        obj=client.sendRqst("localhost",SOCKET_SERVER_PORT,bytes("runServer:%s\n" % socket_port, 'UTF-8'))
    except ConnectionRefusedError:
        pass
    finally:
        client.close()
        return obj


# def stop_htm_server(socket_port):
#     client=socketModule()
#     try:
#         obj=client.sendRqst("localhost",socket_port,bytes("exit", 'UTF-8'))
#     except ConnectionRefusedError:
#         client.close()
#         return False
#     return True


# def send(socket_port, data):
#     client=socketModule()
#     obj=client.sendRqst("localhost",socket_port,bytes(data, 'UTF-8'))


def receive(socket_port):
    client=socketModule()
    obj=client.sendRqst("localhost",socket_port,bytes("get", 'UTF-8'))

    return obj


if __name__ == '__main__':
    pass