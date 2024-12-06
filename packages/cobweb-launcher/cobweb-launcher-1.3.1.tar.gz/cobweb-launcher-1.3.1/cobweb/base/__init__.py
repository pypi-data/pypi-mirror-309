import time
import traceback
import threading

from functools import wraps
from inspect import isgenerator
from typing import Callable, Union

from .common_queue import Queue
from .response import Response
from .basic import Seed, Request, Response
from .item import BaseItem, ConsoleItem
# from .seed import Seed
from .log import logger
# from .dotting import LoghubDot


class TaskQueue:
    TODO = Queue()          # 任务种子队列
    DOWNLOAD = Queue()      # 下载任务队列

    SEED = Queue()          # 添加任务种子队列
    REQUEST = Queue()       # 请求队列
    RESPONSE = Queue()      # 响应队列
    DONE = Queue()          # 下载完成队列
    UPLOAD = Queue()        # 任务上传队列
    DELETE = Queue()        # 任务删除队列

    # DOT = LoghubDot()

    @staticmethod
    def is_empty():
        total_length = TaskQueue.SEED.length
        total_length += TaskQueue.TODO.length
        total_length += TaskQueue.REQUEST.length
        total_length += TaskQueue.DOWNLOAD.length
        total_length += TaskQueue.RESPONSE.length
        total_length += TaskQueue.UPLOAD.length
        total_length += TaskQueue.DONE.length
        total_length += TaskQueue.DELETE.length
        return not bool(total_length)

    @staticmethod
    def process_task(it: Union[Seed, Request, Response, BaseItem], crawler_func: Callable):
        try:
            iterators = crawler_func(it)
            if not isgenerator(iterators):
                raise TypeError(f"{crawler_func.__name__} function isn't a generator")
            for tk in iterators:
                if isinstance(tk, Request):
                    TaskQueue.REQUEST.push(tk)
                elif isinstance(tk, Response):
                    TaskQueue.RESPONSE.push(tk)
                elif isinstance(tk, BaseItem):
                    TaskQueue.UPLOAD.push(tk)
                elif isinstance(tk, Seed):
                    TaskQueue.SEED.push(tk)
                else:
                    raise TypeError(f"{crawler_func.__name__} function return type isn't supported")
                # TaskQueue.DOT.build(
                #     topic=f"{self.project}:{self.task}",
                #     cost_time=end_time - start_time,
                #     **download_item.to_dict
                # )
                # todo: 数据打点
        except Exception as e:
            it.params.retry += 1
            if isinstance(it, Request):
                TaskQueue.REQUEST.push(it)
            elif isinstance(it, Response):
                TaskQueue.RESPONSE.push(it)
            elif isinstance(it, Seed):
                TaskQueue.SEED.push(it)
            time.sleep(1)


class Decorators:

    @staticmethod
    def add_thread(num=1):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args):
                for i in range(num):
                    name = func.__name__ + "_" + str(i) if num > 1 else func.__name__
                    self._threads.append(threading.Thread(name=name, target=func, args=(self,) + args))

            return wrapper

        return decorator

    @staticmethod
    def pause(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            while not self.pause.is_set():
                try:
                    func(self, *args, **kwargs)
                except Exception as e:
                    logger.info(f"{func.__name__}: " + str(e))
                finally:
                    time.sleep(0.1)
            logger.info(f"{func.__name__}: close!")

        return wrapper

    @staticmethod
    def stop(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            while not self.stop.is_set():
                try:
                    func(self, *args, **kwargs)
                except Exception as e:
                    logger.info(
                        f"{func.__name__} exception: \n" +
                        ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                    )
                finally:
                    time.sleep(0.1)

        return wrapper

    @staticmethod
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
