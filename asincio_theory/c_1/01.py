import threading
import time


def hello_from_thread():
    print(f'Hello from thread {threading.current_thread()}!')
    print(f'Hello------------------------- {threading.current_thread().name}!')


hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name
time.sleep(1)
print(f'Python is currently running {total_threads} thread(s)')
print(f'The current thread is {thread_name}')

hello_thread.join()
