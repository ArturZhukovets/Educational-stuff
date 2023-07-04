"""
Yield'ы дают следующие преимущества: когда мы доходим до выполнения блокирующих функций типа `accept()`, `recv()`,
`send()`, Генератор отдаёт мне кортеж с сокетом (серверным или клиентским). Вместо того чтобы зависнуть в ожидании.
Получается, что в этот момент функция ставится на паузу и её выполнения продолжится только тогда, когда сокет
будет готов выполнить этот метод без задержек. И в этот момент цель заключается в том, чтобы поймать момент, когда
данный метод можно будет выполнить без задержек и отправить его в функцию select().

Select() в свою очередь занимается тем, что делает выборку тех сокетов, которые уже готовы и как только что-то готово
вызываем метод next() у соответствующего генератора.


"""

import socket
from select import select
from collections import deque
from typing import Generator

tasks: deque = deque()  # Список событий / задач

to_read = {}
to_write = {}

def server() -> Generator:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - IP/4 | SOCK_STREAM - TCP protocol
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5001))
    server_socket.listen()

    while True:

        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # read
        print("[INFO] Connection from:", addr)

        tasks.append(client(client_socket))


def client(client_socket) -> Generator:
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)  # read
        print("[INFO]: A message has arrived...")
        print(f"[MSG]: {request.decode('utf-8')}")

        if not request:
            break
        else:
            response = "Hello from server, client\n"

            yield ('write', client_socket)
            client_socket.send(response.encode())  # write

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:
            # Ключи словарей `to_read`, `to_write`  - являются сокетами(файловыми дескрипторами).
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task: Generator = tasks.popleft()

            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print("Done")
            pass


if __name__ == '__main__':
    tasks.append(server())
    event_loop()

