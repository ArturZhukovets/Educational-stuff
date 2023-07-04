"""
Сопрограммы по своей сути - это генераторы, которые во время своей работы могут ПРИНИМАТЬ извне какие-то данные.
Реализуется это с помощью метода send(), применимого к генератору.

После того как функции генератору передали send(None) управление 'сдвинулось' до следующего yield (справа от знака равно).
Данное действие "по первоначальной инициации" генератора - это обязательное действие для создания сопрограммы.
Операция, эквивалентная методу `g.send(None)` - это простой вызов метода next(g)

После второй передачи методом send("OK") - значение `OK` было записано в переменную `message`
 и было распечатано print'ом.

Функция `average_coroutine`.
 В коде выполнения данной сопрограммы процесс выполнения происходит в бесконечном цикле. Т.е в теории, сколько угодно
 данных, я бы не передал, я бесконечно буду получать response от `yield`. Однако, в качестве входного значения, можно
 пробросить любое исключение (Exception) даже кастомный, используя метод `throw()`

Внутри такого генератора можно использовать ключевое слово `return`.
 В таком случае значение, получаемое после `return` можно получить ТОЛЬКО перехватив StopIteration исключение
 и обратившись к атрибуту `value` у объекта исключения (99 строка).
"""
from inspect import getgeneratorstate
from typing import Generator


def sub_gen() -> Generator:
    """Данная функция является генератором."""
    x: str = "Ready to accept message"
    message = yield x
    print("[INFO] Subgen received", message)


g = sub_gen()

print("[INFO] generator state:", getgeneratorstate(g))  # 'GEN_CREATED'


g.send(None)  # Инициализировали
# next(g)  # Эквивалентно
print("[INFO] generator state after `send(None)`:", getgeneratorstate(g))  # 'GEN_SUSPENDED'

try:
    g.send("Ok")  # StopIteration и print()
except StopIteration:
    print("[INFO] Done! End of the job of generator.")

########################################################################################

class CustomUsefulException(Exception):
    pass

def coroutine_initialization(func):
    """
    Декоратор, принимающий на вход сопрограмму(генераторную функцию).
    Задача которого инициализировать генератор.
    """
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


@coroutine_initialization
def average_coroutine() -> Generator:
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print("Done. StopIteration.")
            break
        except CustomUsefulException:
            # Some useful work here
            print("########### Done. Ended by CustomException. ###########")
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)

    return average


gen = average_coroutine()  # Инициализация генератора происходит за счёт декоратора
first = gen.send(4)
print("avg is - ", first)
second = gen.send(5)
print("avg is - ", second)
third = gen.send(6)
print("avg is - ", third)
forth = gen.send(30)
print("avg is - ", forth)

try:
    gen.throw(CustomUsefulException)  # Прокидываю исключение
except StopIteration as e:
    print('Average after stop is -', e.value)
    returned_value = e.value  # Финальное значение от return

# after_exc = gen.send(50_000)
# print(after_exc)







