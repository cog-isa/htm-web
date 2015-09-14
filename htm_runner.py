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
from sockets import SocketServer
from htm_core_class import HTMCore
import jsonpickle

active_ports = set()

#  In order to start using WTForms-JSON, you need to first initialize the extension.
#  This monkey patches some classes and methods within WTForms and adds JSON handling support
wtforms_json.init()

class HTMSerialization:
    pass


def start_htm(server_port, settings_id):

    setjson=RunSettings.select().where(RunSettings.id==settings_id).get()
    f = SettingsForm.from_json(jsonpickle.json.loads(setjson.json_string), skip_unknown_keys=True)
    inset = f.getInputSettings()
    spset = f.getSpatialSettings()
    tpset = f.getTemporalSettings()

    htm = HTMCore(inset, spset, tpset)
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
    message = runner_server.receive_message()
    (port,settings_id)=message.replace('(','',1).replace(')','',1).split(',')
    (port,settings_id)=(int(port),int(settings_id))
    if port not in active_ports:
        print(port)
        active_ports.add(port)
        thread = threading.Thread(target=start_htm, args=(port, settings_id,))
        thread.daemon = True
        thread.start()
    runner_server.send_message("")
