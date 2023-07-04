import asyncio

from asyncio import CancelledError
from asincio_theory.util import delay


#########################################################################

async def cancel_task():
    """
    В данной сопрограмме начинает выполняться какая-то длительная операция, работающая 15с.
    Внутри цикла while идёт проверка завершена ли данная задача. done() - возвращает True если задача завершилась,
     в противном случае - False. Каждую секунду идёт проверка и если не уложились в 5 секунд - метод `cancel()`
     завершает задачу и уже в await `long_task` обрабатывается исключением CanceledError.

    CanceledError может быть возбуждено только внутри `await`
    """
    long_task = asyncio.create_task(delay(15))

    seconds_elapsed = 0

    while not long_task.done():
        print("Начали выполнять все таски...")
        await asyncio.sleep(1)
        print("Задача ещё не закончилась. Проверка каждую секунду.")
        seconds_elapsed += 2

        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
        print("Задача успела завершиться.")
    except CancelledError:
        print("Задача была снята по истечению 5 секунд.")

# asyncio.run(cancel_task())

#########################################################################

async def time_out_task():
    """
    Данная программа запускается, используя функцию `wait_for`, которая задаёт тайм-аут.
    По истечении времени тайм-аута возбуждается исключение TimeoutError.
    """
    long_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(long_task, timeout=5)
        print(result)
    except asyncio.TimeoutError:
        print("Тайм-аут! Отведённое время вышло, снимаем задачу.")
        print(f"Задача была снята? {long_task.cancelled()}")

asyncio.run(time_out_task())

########################################################################
