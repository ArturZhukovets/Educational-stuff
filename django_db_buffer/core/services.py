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
            buffer.update(message)
    finally:
        buffer.release_buffer()
    print("Records were updated")


def record_and_update():
    with get_buffer("logs"):
        record = _create()
        record_to_db()
        _update(record)
    debug = True
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





# add(inst1)
# add(inst2)