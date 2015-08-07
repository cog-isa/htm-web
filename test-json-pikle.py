import socket


__author__ = 'AVPetrov'
import temporalPooler
from temporalPooler.htm_cell import Cell
from temporalPooler import htm_column
from temporalPooler import util
import pickle




host = "localhost"
SOCKET_PORT = 11101

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, SOCKET_PORT))

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

sock.sendall(bytes("get:\n", 'UTF-8'))
end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"

data = bytes()

while True:
    q = sock.recv(1024)
    try:
        if q.decode('utf-8').find(end_message) == -1:
            break
    except UnicodeDecodeError:
        pass
    data += q

sock.close()
# data = sock.recv(10024)
obj = pickle.loads(data)
print(obj)
obj.out_prediction()
exit(0)





# An arbitrary collection of objects supported by pickle.
data = {
    'a': [1, 2.0, 3, 4+6j],
    'b': ("character string", b"byte string"),
    'c': set([None, True, False])
}

with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


with open('data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)