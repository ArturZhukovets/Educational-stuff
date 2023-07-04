"""
    Делегирующий генератор.
Делегирующий генератор - это тот генератор, который вызывает какой-нибудь другой.
Соответственно, подгенератор - это вызываемый генератор.

Такая конструкция используется когда необходимо разбить один генератор на несколько.(как с функциями)

`yield from` Конструкция как видно из примера ниже не только заменяет цикл `while True:` в ДЕЛЕГИРУЮЩЕМ ГЕНЕРАТОРЕ,
 но также эта конструкция берёт на себя передачу данных в подгенератор (`sub_gen.send()`),
  берёт на себя передачу исключений (`sub_gen.throw(ex)`). Получает возвращаемый с помощью `return` от подгенератора
  результат.

`yield from` - в других языках это тот же самый `await`. На практике он напрямую управляет работой подгенератора.
Соответственно, пока это происходит (работа подгенератора) делегирующий генератор вынужден "Ожидать(await)"
 пока подгенератор не завершит свою работу.

Исходя их этого получается, что ПОДГЕНЕРАТОР должен иметь механизм, позволяющий завершать его работу.
Иначе ДЕЛЕГИРУЮЩИЙ генератор будет навечно заблокирован.

Строго говоря `yield from` просто yield'ит результат из любого итерируемого объекта.

"""
from typing import Generator


def sub_gen():
    """Это читающий генератор, который мы вызываем (буквально как некая рабочая функция)"""
    for i in "Artur":
        yield i

def delegator(g: Generator):
    """Это транслятор. Который вызывает читающий генератор"""
    for i in g:
        yield i


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


#####################################################################
"""Здесь имеем дело с обычными генераторами"""
sg = sub_gen()
g = delegator(sg)

print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
# print(next(g))  # StopIteration
#######################################################################
"""Здесь пойдёт код, работающий с coroutine"""

@coroutine_initialization
def subgen_coroutine():
    while True:
        try:
            message = yield
        except (StopIteration, CustomUsefulException):
            print("Пришло исключение от делегирующего генератора.")
            print("################ EXCEPTION ################")
            print("Исключение обработано. Сейчас выбросится наверх `StopIteration...`")
            break
        else:
            print("[INFO] Подгенератор выполняет работу...")
            print('PROCESSING...', message)
    return "Returned from `subgen()`"

@coroutine_initialization
def delegator_coroutine(sub_gen: Generator):
    """
    Делегирующий генератор должен принять значение и затем отдать его в подгенератор.
    `yield from sub_gen` Эквивалентно закомментированному коду.
    """
    # while True:
    #     try:
    #         data = yield
    #         sub_gen.send(data)
    #     except (StopIteration, CustomUsefulException) as ex:
    #         print("Делегирующий генератор закончил свою работу после исключения.")
    #         print("Пробрасываем исключение подгенератору...")
    #         try:
    #             sub_gen.throw(ex)
    #             break
    #         except StopIteration as e:
    #             print("В делегирующем генераторе теперь отловлено исключение от подгенератора...")

    result_from_subgen = yield from sub_gen
    # some processing of subgen result
    print(result_from_subgen)


sg = subgen_coroutine()
g = delegator_coroutine(sg)
g.send("Message from user...")
g.send("other message...")
try:
    g.throw(CustomUsefulException)
except StopIteration as e:
    print("...")
