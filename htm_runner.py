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


#  In order to start using WTForms-JSON, you need to first initialize the extension.
#  This monkey patches some classes and methods within WTForms and adds JSON handling support



class HTMSerialization:
    pass


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
        print(message)
        if SystemMessages.GET_DATA in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            htm_serialization = HTMSerialization()
            htm_serialization.input = htm.input
            htm_serialization.compress_input = htm.compress_input
            htm_serialization.temporal_pooler = htm.temporal_pooler

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            htm_serialization = HTMSerialization()
            htm.move()
            htm_serialization.input = htm.input
            htm_serialization.compress_input = htm.compress_input
            htm_serialization.temporal_pooler = htm.temporal_pooler

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE10 in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            htm_serialization = HTMSerialization()
            for i in range(10):
                htm.move()
            htm_serialization.input = htm.input
            htm_serialization.compress_input = htm.compress_input
            htm_serialization.temporal_pooler = htm.temporal_pooler

            server.send_message(jsonpickle.encode(htm_serialization))
            continue

        if SystemMessages.MOVE100 in message:
            # сериализуем нужные нам части в объекте HTMSerialization
            htm_serialization = HTMSerialization()
            for i in range(100):
                htm.move()
            htm_serialization.input = htm.input
            htm_serialization.compress_input = htm.compress_input
            htm_serialization.temporal_pooler = htm.temporal_pooler

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
            print("restart_ok")
            continue

        if SystemMessages.STOP in message:
            server.send_message("ok")
            server.close()
            print("close")
            break

        print("Сообщение не обработано, нет ключей или .п.")


if __name__ == "__main__":
    active_ports = set()
    wtforms_json.init()

    runner_server = SocketServer(10100)

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
                print("olololo")
            else:
                active_ports.add(port)
                thread = threading.Thread(target=start_htm, args=(port, settings_id,))
                thread.daemon = True
                thread.start()

        runner_server.send_message("")
