import sys
import wtforms_json
from models import RunSettings
from settingsform import SettingsForm

sys.path.insert(0, "htm-core/")
sys.path.insert(0, "htm-core/spatialPooler")
sys.path.insert(0, "htm-core/temporalPooler")
sys.path.insert(0, "htm-core/gens")
sys.path.insert(0, "htm-core/apps")

import threading
from sockets import SocketServer, SystemMessages, SocketClient
from htm_core_class import HTMCore
import jsonpickle


class HTMSerialization:
    def __init__(self, htm):
        self.input = htm.input
        self.compress_input = htm.compress_input
        self.temporal_pooler = htm.temporal_pooler


def start_htm(server_port, settings_id):
    setjson = RunSettings.select().where(RunSettings.id == settings_id).get()
    f = SettingsForm.from_json(jsonpickle.json.loads(setjson.json_string), skip_unknown_keys=True)
    inset = f.getInputSettings()
    spset = f.getSpatialSettings()
    tpset = f.getTemporalSettings()

    htm = HTMCore(inset, spset, tpset)
    htm.move()
    # десиреализовать объект из строки - jsonpickle.decode(s)

    server = SocketServer(server_port)

    while True:
        data = server.receive_message()
        message = SystemMessages.get_keys_in_text(data)
        data = SystemMessages.clear_keys_in_text(data)
        if SystemMessages.GET_DATA in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            htm_serialization = HTMSerialization(htm)

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE in message:
            # сериализуем нужные нам части в объекте HTMSerialization

            htm.move()
            htm_serialization = HTMSerialization(htm)
            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE10 in message:
            # сериализуем нужные нам части в объекте HTMSerialization

            for i in range(10):
                htm.move()
            htm_serialization = HTMSerialization(htm)

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE100 in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            for i in range(100):
                htm.move()
            htm_serialization = HTMSerialization(htm)

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.RESTART_WITH_SETTINGS:
            port, settings_id = data.replace('(', '', 1).replace(')', '', 1).split(',')
            setjson = RunSettings.select().where(RunSettings.id == settings_id).get()
            f = SettingsForm.from_json(jsonpickle.json.loads(setjson.json_string), skip_unknown_keys=True)
            inset = f.getInputSettings()
            spset = f.getSpatialSettings()
            tpset = f.getTemporalSettings()

            htm = HTMCore(inset, spset, tpset)
            htm.move()
            server.send_message("ok")
            continue

        if SystemMessages.STOP in message:
            server.send_message("ok")
            server.close()
            break

        print("Сообщение не обработано, нет ключей или .п.")


if __name__ == "__main__":
    #  In order to start using WTForms-JSON, you need to first initialize the extension.
    #  This monkey patches some classes and methods within WTForms and adds JSON handling support
    #  wtf ????
    wtforms_json.init()

    active_ports = set()

    running_port = 10100
    runner_server = SocketServer(running_port)
    print(" * Running on port %d (Press CTRL+C to quit)" % running_port)
    while True:
        data = runner_server.receive_message()
        message = SystemMessages.get_keys_in_text(data)
        data = SystemMessages.clear_keys_in_text(data)

        if SystemMessages.TURN_ON_HTM_WITH_SETTINGS in message:
            (port, settings_id) = data.replace('(', '', 1).replace(')', '', 1).split(',')
            (port, settings_id) = (int(port), int(settings_id))
            if port in active_ports:
                client = SocketClient(port)
                client.request((port, settings_id), SystemMessages.RESTART_WITH_SETTINGS)
                client.close()
            else:
                active_ports.add(port)
                thread = threading.Thread(target=start_htm, args=(port, settings_id,))
                thread.daemon = True
                thread.start()

        runner_server.send_message("")
