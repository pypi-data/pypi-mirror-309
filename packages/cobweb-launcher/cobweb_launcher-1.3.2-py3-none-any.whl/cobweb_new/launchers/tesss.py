import threading
import time
from functools import wraps


def add_thread(num=1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args):
            for i in range(num):
                name = func.__name__ + "_" + str(i) if num > 1 else func.__name__
                self._threads.append(threading.Thread(name=name, target=func, args=(self,) + args))
        return wrapper

    return decorator


def pause(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(str(e))
            finally:
                time.sleep(0.1)

    return wrapper


class TTT:
    _threads = []

    @add_thread()
    @pause
    def tt(self):
        print("hello")
        time.sleep(1)

tttt = TTT()
tttt.tt()
print(TTT._threads)


for _ in TTT._threads:
    _.start()
