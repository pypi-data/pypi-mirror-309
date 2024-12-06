import time
import threading

from abc import ABC, abstractmethod
from cobweb.base import BaseItem, TaskQueue, logger, Decorators
from cobweb import setting


class Pipeline(ABC):

    def __init__(
            self,
            pause: threading.Event,
    ):
        super().__init__()
        self.pause = pause
        self.upload_queue_size = setting.UPLOAD_QUEUE_SIZE
        self.upload_wait_time = setting.UPLOAD_WAIT_TIME

    @abstractmethod
    def build(self, item: BaseItem) -> dict:
        ...

    @abstractmethod
    def upload(self, table: str, data: list) -> bool:
        ...

    @Decorators.pause
    def run(self):
        data_info, seeds = {}, []
        thread_sleep = self.upload_wait_time if TaskQueue.UPLOAD.length < self.upload_queue_size else 0.1
        try:
            while item := TaskQueue.UPLOAD.pop() and len(seeds) <= self.upload_queue_size:
                data = self.build(item)
                data_info.setdefault(item.table, []).append(data)
                seeds.append(item.seed)
            for table, datas in data_info.items():
                self.upload(table, datas)
        except Exception as e:
            logger.info(e)
            seeds = None
        finally:
            TaskQueue.DONE.push(seeds)

        time.sleep(thread_sleep)
