"""
Написать декоратор, инициализирующий coroutine.
Написать сопрограмму на генераторах, принимающую сообщение от пользователя.
Она регистрирует сообщение и отдаёт предыдущее сообщение. Как только в буфере 100 сообщений,
сопрограмма ВОЗРАЩАЕТ значение самого популярного (или рандомного слова).
"""
import random
from typing import Generator, Callable


def coroutine_init(func: Callable):
    def inner(*args, **kwargs) -> Generator:
        print("[INFO] initialize coroutine...")
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


@coroutine_init
def message_coroutine(attempts: int) -> Generator[str, None, str]:
    message_counter = 0
    register = {}

    while True:

        try:
            if message_counter == attempts:
                raise StopIteration
            response_for_user = register[message_counter-1] if (register and message_counter > 1) else None
            message = yield response_for_user

            message_counter += 1
            register[message_counter] = message
            print("[INFO] The counter has increased by one...")
        except StopIteration:
            print(f"[INFO] {attempts} messages have been received finishing the generator.")
            break

    the_most_popular_word_ind = random.randint(1, attempts)
    return register[the_most_popular_word_ind]


if __name__ == '__main__':
    num = 5
    g = message_coroutine(num)
    try:
        for i in range(num):
            response = g.send(input("Enter your message: "))
            print(f"Generators response -  {response}")
    except StopIteration as e:
        final = e.value
        print(f"Final answer - {final}")


