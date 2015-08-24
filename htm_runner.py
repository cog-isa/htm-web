import threading
from sockets import SocketServer
from htm_core_class import HTMCore
import jsonpickle


active_ports = set()


def start_htm(port):
    htm = HTMCore()
    server = SocketServer(port)

    while True:
        message = server.receive_message()
        htm.temporal_pooler.step_forward(htm.generator.get_data())
        htm.generator.move()
        server.send_message(jsonpickle.encode(htm))
        print(jsonpickle.encode(htm))

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