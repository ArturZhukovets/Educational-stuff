"""
Using telnet or nc localhost 5001 I can have a connection with `server_socket`
Server wait this connection.
And after establishing a connection server wait a message from client.
After receiving the message, the server processes it and return a response.
Before performing each operation, the server is blocked and
 at this moment it cannot accept requests from other users.
"""

import socket

# domain:5001

users_counter = 0
users = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - IP/4 | SOCK_STREAM - TCP protocol
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5001))
server_socket.listen()

def get_user(addr: str) -> int:
    global users_counter, users
    if addr not in users:
        users_counter += 1
        users[addr] = users_counter
        print(f"[INFO]: Пользователь # {users[addr]} был добавлен")
    else:
        print(f"[INFO]: Пользователь # {users[addr]} уже существует")
    return users[addr]


while True:
    # Читает буфер. И если что-либо пришло возвращает кортеж из 2 элементов
    # 1 - сокет с другой стороны (client_socket) и адрес (address)
    print("Before .accept() -> Ждём подключения...")
    client_socket, address = server_socket.accept()
    str_address: str = ":".join(map(str, address))
    print("[INFO]: Появилось соединение с пользователем:", address)
    print("[INFO]: Регистрируем пользователя...")
    user = get_user(str_address)

    while True:
        print(f"Before .recv() -> Ждём сообщения от пользователя... {user}")
        request = client_socket.recv(4096)
        print(f"Сообщение от пользователя: {request.decode('utf-8')}")
        if not request:
            break
        else:

            response = "Hello user with address: %s\n" % str_address
            client_socket.send(response.encode())

    print(f"Закончили соединение с пользователем {user}")
    print("Можно принимать другого пользователя...")
    client_socket.close()


