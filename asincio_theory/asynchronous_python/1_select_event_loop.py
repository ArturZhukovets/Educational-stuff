"""
При вызове метода server_socket.bind(("localhost", 5001)),
 внутри системы создаётся файл сокета. Метод select() работает с любым объектом у которого есть файловый дескриптор
 (а файловый дескриптор по сути есть у любого файла).
select() - принимает на вход 3 списка:
 1 список - это объекты, за которыми необходимо следить, которые доступны для чтения.
 2 список - это объекты, за которыми необходимо следить, которые доступны для записи.
 3 список - это объекты у которых ожидаем какие-либо ошибки
 Данный метод возвращает те же списки, НО после того как они станут доступны (для чтения, записи, или ошибки)
"""

import socket
from select import select

# domain:5001

to_monitor = []
users_counter = 0
users = {}

def accept_connection(server_socket):
    """
    На вход поступает объект сокета. Происходит его обработка.
    Читает буфер. И если что-либо пришло возвращает кортеж из 2 элементов
    сокет с другой стороны (client_socket) и адрес (address)
    """
    client_socket, address = server_socket.accept()
    str_address: str = ":".join(map(str, address))
    print("[INFO]: Обслуживаем соединение с:", str_address)
    print("[INFO]: Регистрируем пользователя...")
    user = get_user(str_address)

    to_monitor.append(client_socket)
    return user

def send_massage(client_socket, user):
    request = client_socket.recv(4096)

    if not request:
        client_socket.close()
        print(f"Закончили соединение с пользователем {user}")
    else:
        print(f"Сообщение от пользователя: {request.decode('utf-8')}")
        response = f"Hello user # {user}\n"
        client_socket.send(response.encode())

def event_loop():
    while True:
        print("[INFO]: Ждём событие...")
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                # user = get_user()
                user = accept_connection(sock)

                print(f"[INFO]: Соединение c пользователем {user} установлено, ждём сообщения...")

            else:
                user = get_user(sock.getpeername())
                print(f"[INFO]: Приняли сообщение от пользователя {user}...")

                send_massage(sock, user)

            print("[INFO]: Прошёл цикл обработки событий, ожидаем следующее...")

def get_user(addr: str) -> int:
    global users_counter, users
    if isinstance(addr, tuple):
        addr = ':'.join(map(str, addr))
    if addr not in users:
        users_counter += 1
        users[addr] = users_counter
        print(f"[INFO]: Пользователь # {users[addr]} был добавлен")
    else:
        pass
    return users[addr]


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - IP/4 | SOCK_STREAM - TCP protocol
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5001))
    server_socket.listen()

    to_monitor.append(server_socket)
    event_loop()
