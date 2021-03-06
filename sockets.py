import socket as _socket
import types


class SystemMessages:
    """
        В этом классе определяются используемые ключи,а также предоставляются методы для работы с этими ключами, в частности
    их поиск в тексте и удаление их из текста
    """
    # ключ для включения htm с настройками
    TURN_ON_HTM_WITH_SETTINGS = "[SYSTEM_MESSAGE_TURN_ON_HTM_WITH_SETTINGS]"
    # ключ для включения без настроек
    TURN_ON_HTM_WITHOUT_SETTINGS = "[SYSTEM_MESSAGE_TURN_ON_HTM_WITHOUT_SETTINGS]"
    # ключ для расчета следующего шага
    MOVE = "[SYSTEM_MESSAGE_MOVE_MOVE_MOVE]"
    # ключ для получения текущей информации
    MOVE100 = "[SYSTEM_MESSAGE_MOVE100]"
    # ключ для получения текущей информации
    MOVE1000 = "[SYSTEM_MESSAGE_MOVE1000]"
    # ключ для получения текущей информации
    GET_DATA = "[SYSTEM_MESSAGE_GET_DATA]"
    # остановить htm сервер
    STOP = "[SYSTEM_MESSAGE_STOP_STOP_STOP]"
    # перезапустить с новыми настройками
    RESTART_WITH_SETTINGS = "[SYSTEM_MESSAGE_RESTART_WITH_SETTINGS]"

    @staticmethod
    def get_keys_in_text(text):
        res = []
        for i in SystemMessages.__dict__:
            key = SystemMessages.__dict__[i]
            key = str(key)
            if key.find("SYSTEM_MESSAGE_") != -1:
                if text.find(key) != -1:
                    res.append(key)
        return res

    @staticmethod
    def clear_keys_in_text(text):
        """
            класса передается строка текста, создается новая строка из которой удалены все вхождения ключей,
        данная строка возвращается, то есть использовать нужно так s = SystemMessages.clear_keys_in_text(s)
        тогда из строки будут удалены все ключи
        :param text: входной текста
        :return: текст без ключей
        """
        for i in SystemMessages.__dict__:
            key = SystemMessages.__dict__[i]
            key = str(key)
            if key.find("SYSTEM_MESSAGE_") != -1:
                text = text.replace(key, "")
        return text


class SocketServer:
    def __init__(self, port):
        self.port = str(port)
        self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.server_address = ('localhost', int(self.port))
        self.socket.bind(self.server_address)
        self.socket.listen(1)
        self.end_message = "[END_MESSAGE]"
        self.connection = None

    def send_message(self, data, message=""):
        self.connection.sendall(bytes(str(data) + message + self.end_message, 'UTF-8'))

    def receive_message(self):
        self.connection, client_address = self.socket.accept()

        res = ""
        while True:
            q = self.connection.recv(1024).decode('utf-8')
            res += q
            if res.find(self.end_message) != -1:
                break

        return res.replace(self.end_message, "")

    def close(self):
        self.socket.close()


class SocketClient:
    # Клиент написан так, что всегда ждет ответа от сокета
    # TODO добавить время ожидания ответа

    def __init__(self, port):
        self.port = port
        self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)

        self.end_message = "[END_MESSAGE]"

    def request(self, data, message=""):
        self.socket.connect(('localhost', self.port))
        self.socket.sendall(bytes(str(data) + message + self.end_message, 'UTF-8'))

        res = ""
        while True:
            q = self.socket.recv(1024).decode('utf-8')
            res += q
            if res.find(self.end_message) != -1:
                break

        return res.replace(self.end_message, "")

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    # тест механизма SystemMessages
    s = "12312" + SystemMessages.TURN_ON_HTM_WITH_SETTINGS + SystemMessages.MOVE
    print(SystemMessages.get_keys_in_text(s))
    print(SystemMessages.clear_keys_in_text(s))
