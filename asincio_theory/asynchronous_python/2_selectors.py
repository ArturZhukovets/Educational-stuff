"""
В данном примере я пользовался регистрацией сокетов используя дефолтный селектор.
Каждый сокет регистрируется вместе с сопровождающими его данными (в данном примере передавалась функция)
Т.е есть сокет и есть связанная с ним функция. И эта пара регистрируется в селекторе.
"""

import socket
import selectors


selector = selectors.DefaultSelector()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - IP/4 | SOCK_STREAM - TCP protocol
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5001))
    server_socket.listen()

    # Зарегистрировали серверный сокет.
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    """
    На вход поступает объект серверного сокета. Происходит его обработка.
    Читает буфер. И если что-либо пришло возвращает кортеж из 2 элементов
    сокет с другой стороны (client_socket) и адрес (address)
    """
    client_socket, address = server_socket.accept()
    str_address: str = ":".join(map(str, address))
    print("[INFO]: Обслуживаем соединение с:", str_address)

    # Зарегистрировали клиентский сокет.
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_massage)
    print("\n", '*' * 20, "\n")

def send_massage(client_socket):
    request = client_socket.recv(4096)
    print("[INFO]: Обслуживание чтения и отправки сообщений")
    print(f"[INFO]: Получено от пользователя:\n{request.decode('utf-8')}")
    if request:
        response = "hello\n"
        client_socket.send(response.encode())
        print("[INFO]: Отправка сообщения пользователю...")
        print("[INFO]: Сообщение отправлено.")
    else:
        print("[INFO]: Закрываем соединение с  пользователем.")
        selector.unregister(fileobj=client_socket)  # Сняли с регистрации клиентский сокет
        client_socket.close()

    print("\n", '#' * 80, "\n")


def event_loop():
    """
    Метод select() возвращает список кортежей.
    Один кортеж на каждый зарегистрированный объект.
    В каждом кортеже имеется key, event.
    Нас сейчас интересует исключительно key. Key - это объект SelectorKey,
     хранящий в себе данные, которые мы заполняли при регистрации selector'а.

    Далее мы для каждого события получаем свою функцию (callback) и в зависимости от того, какой селектор пришёл,
     С той функцией мы и работаем. (В этом случае с accept_connection() или с send_massage() функциями.)
    """

    while True:

        print("[INFO]: Слушаем событие...")
        events = selector.select()   # -> (key, events)
        print("[INFO]: Пришло событие. Уточняем, что за событие по его `.data`...")
        for key, _ in events:  # key: SelectorKey
            callback = key.data
            callback(key.fileobj)  # fileobj - Это сам сокет (серверный или клиентский)


if __name__ == '__main__':
    server()
    event_loop()
