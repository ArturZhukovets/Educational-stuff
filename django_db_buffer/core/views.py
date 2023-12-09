import random
import time
import multiprocessing
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .services import record_to_db, update_in_db, record_and_update, record_to_db_in_two_threads
from .models import TextLog
# Create your views here.


def index(request):
    messages = list(TextLog.objects.values_list("message", flat=True))
    return JsonResponse({"msgs": messages})


def start_record(request):
    process = multiprocessing.Process(target=record_to_db)
    process.start()
    return redirect("index")


def update_record(request):
    process = multiprocessing.Process(target=update_in_db)
    process.start()
    return redirect("index")

def delete_records(request):
    logs = TextLog.objects.all()
    logs.delete()
    return redirect("index")


def both_update_and_create_records(request):
    process = multiprocessing.Process(target=record_and_update)
    process.start()
    return redirect("index")
    # TODO Реализовать тест кейс при котором будет несколько раз вызываться один и тот же
    # TODO getBuffer(__name__) и убедиться, что там будет одинаковый storage.


def thread_manipulation_with_instance(request):
    log = TextLog.objects.first()
    if not log:
        return JsonResponse({"msg": "Log record was not founded"})
    process = multiprocessing.Process(target=record_to_db_in_two_threads, args=[log])
    process.start()
    return redirect("index")
