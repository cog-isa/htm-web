import threading
from sockets import SocketServer
from htm_core_class import HTMCore
import jsonpickle


active_ports = set()


class HTMSerialization:
    pass


def start_htm(server_port):
    htm = HTMCore()
    # десиреализовать объект из строки - jsonpickle.decode(s)

    server = SocketServer(server_port)

    while True:
        # сообщение в будущем нужно будет обрабатывать
        # message = server.receive_message()
        server.receive_message()

        # сериализуем нужные нам части в объекте HTMSerialization
        htm_serialization = HTMSerialization()
        htm.move()
        htm_serialization.input = htm.input
        htm_serialization.compress_input = htm.compress_input
        htm_serialization.temporal_pooler = htm.temporal_pooler

        server.send_message(jsonpickle.encode(htm_serialization))
        print(jsonpickle.encode(htm_serialization))


runner_server = SocketServer(10100)

while True:
    port = runner_server.receive_message()
    if port not in active_ports:
        print(port)
        active_ports.add(port)
        thread = threading.Thread(target=start_htm, args=(port,))
        thread.daemon = True
        thread.start()
    runner_server.send_message("")