import asyncio
from asyncio import CancelledError

from asincio_theory.util import delay

# 2.8
async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    res = await sleep_for_three
    print(res)

# 2.9
async def several_tasks():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(4))
    sleep_once_more = asyncio.create_task(delay(5))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


# 2.10
async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("Пока я жду исполняется другой код...")
    print("Другой код выполнился, а я всю ещё жду")

async def main_2():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay


# asyncio.run(main_2())

# 2.11 Снятие задачи
async def main_3():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0
    while not long_task.done():
        print("Задача ещё не закончилась, следующая проверка через секунду...")
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print("Задача была снята.")

asyncio.run(main_3())
