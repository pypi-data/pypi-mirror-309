import time
import threading
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
    def wrapper(self, *args, **kwargs):
        while not self.pause.is_set():
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                pass
                # logger.info(f"{func.__name__}: " + str(e))
            finally:
                time.sleep(0.1)

    return wrapper


def stop(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        while not self.stop.is_set():
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                # logger.info(f"{func.__name__}: " + str(e))
                pass
            finally:
                time.sleep(0.1)

    return wrapper


def decorator_oss_db(exception, retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(callback_func, *args, **kwargs):
            result = None
            for i in range(retries):
                msg = None
                try:
                    return func(callback_func, *args, **kwargs)
                except Exception as e:
                    result = None
                    msg = e
                finally:
                    if result:
                        return result

                    if i >= 2 and msg:
                        raise exception(msg)

        return wrapper

    return decorator



