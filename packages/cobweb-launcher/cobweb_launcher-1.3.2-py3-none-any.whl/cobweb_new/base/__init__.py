import time
from inspect import isgenerator
from typing import Callable, Union

from .common_queue import Queue
from .response import Response
from .request import Request
from .item import BaseItem, ConsoleItem
from .seed import Seed

from .log import logger
# from .decorators import decorator_oss_db, stop, pause
import decorators


class TaskQueue:

    SEED = Queue()          # 添加任务种子队列
    TODO = Queue()          # 任务种子队列
    REQUEST = Queue()       # 请求队列

    DOWNLOAD = Queue()      # 下载任务队列
    RESPONSE = Queue()      # 响应队列
    DONE = Queue()          # 下载完成队列

    UPLOAD = Queue()        # 任务上传队列

    DELETE = Queue()        # 任务删除队列

    def __init__(self, db):
        self.db = db

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
    # @staticmethod
    # def distribute(it):

    @staticmethod
    def process_task(it: Union[Seed, Request, Response, BaseItem], crawler_func: Callable):
        try:
            iterators = crawler_func(it)
            if not isgenerator(iterators):
                raise TypeError(f"{crawler_func.__name__} function isn't a generator")
            for tk in iterators:
                if isinstance(tk, Request):
                    TaskQueue.DOWNLOAD.push(tk)
                elif isinstance(tk, Response):
                    TaskQueue.RESPONSE.push(tk)
                elif isinstance(tk, BaseItem):
                    TaskQueue.UPLOAD.push(tk)
                elif isinstance(tk, Seed):
                    TaskQueue.SEED.push(tk)
        except Exception as e:
            if not isinstance(it, BaseItem):
                it.seed.params.retry += 1

            time.sleep(5)


class Distribute:
    """
    数据分发器，将数据分发到各个队列中
    """