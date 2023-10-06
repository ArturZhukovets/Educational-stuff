import threading
import time
import random
from db_buffer_service import get_buffer
from django.db import connection

from .models import TextLog

messages = ["message first", "super message", "strange message"]


def record_to_db() -> None:
    # quer
    buffer = get_buffer("logs")
    try:
        for i in range(10):
            message = str(i)
            text_log = TextLog(message=message)
            buffer.add(text_log)
            # time.sleep(1)
    finally:
        print(f"Buffer empty?: {buffer.buffer_is_empty()}")
    print("Cycle records were handled")


def update_in_db() -> None:
    buffer = get_buffer("logs")

    try:
        message = TextLog.objects.first()
        for i in range(5):
            if not message:
                break
            message.message = random.choice(messages)
            message.some_str_field = "Hello, world!"
            print("#" * 40)
            print(f"in cycle: {message}")
            print("#" * 40)
            buffer.update(message, update_fields=['message'])
    finally:
        buffer.release_buffer()
    message.refresh_from_db()
    print("\n\n")
    print("--" * 40)
    print(f"Final: {message}")
    print("--" * 40)
    print("Records were updated")


def record_and_update():
    with get_buffer("logs"):
        record = _create()
        record_to_db()
        _update(record)
    # buffer.release_buffer()

def _create():
    buffer = get_buffer("logs")

    try:
        record = TextLog(message="Record before update")
        buffer.add(record)
    finally:
        print(f"Buffer empty?: {buffer.buffer_is_empty()}")
    print(f"Before: {record.message}")
    return record


def _update(record):
    buffer = get_buffer("logs")
    try:
        record.message = "Record after update!!!"
        buffer.update(record)
    finally:
        print(f"Buffer empty?: {buffer.buffer_is_empty()}")
    print(f"After: {record.message}")


def record_to_db_in_two_threads(log: TextLog):
    buffer = get_buffer("logs")
    log_pk = log.pk
    thread_execution_func(log_pk)

    # time.sleep(1)
    for i in range(4):
        log.message = "Actual message!!!"
        log.save(update_fields=["message"])
        # log.save()
        print("#" * 40)
        print("Log record inside [MAIN-Thread]:")
        print(log)
        print("#" * 40)

        time.sleep(3)
    log.refresh_from_db()
    print("--" * 40)
    print("FINAL STATE OF LOG RECORD: ")
    print(log)
    print("--" * 40)
    print("\nEnd of the process...")

def thread_execution_func(log_pk: int):

    def _execution(log_pk: int):
        # while True:
        time.sleep(1)
        log = TextLog.objects.get(pk=log_pk)
        cur_timestamp = int(time.time())
        log.some_str_field = cur_timestamp
        log.some_choices_field = log.random_choice()
        log.message = "will be overwritten"
        log.save()
        print("*" * 40)
        print("Log record inside [CHILD-Thread]:")
        print(log)
        print("*" * 40)
        # time.sleep(5)

    thread = threading.Thread(target=_execution, args=[log_pk], daemon=True)
    thread.start()

# TODO Теория подвердилась. Объект необзодимо обновлять либо забирая его актуальную версию из базы либо обновляя
#  только определённые филды.
#  TODO попробовать завтра написать внутри Buffer логику, позволяющую обновлять только указанные филды.



