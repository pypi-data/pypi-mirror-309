import json
import time
import threading
from typing import Union, Callable, Mapping

import setting
from cobweb.base import (
    Seed,
    BaseItem,
    Request,
    Response,
    ConsoleItem,
    decorators,
    TaskQueue,
    logger
)
from constant import DealModel


class Crawler(threading.Thread):

    def __init__(self, custom_func: Union[Mapping[str, Callable]]):
        super().__init__()

        for func_name, _callable in custom_func.items():
            if isinstance(_callable, Callable):
                self.__setattr__(func_name, _callable)

        self.spider_max_retries = setting.SPIDER_MAX_RETRIES
        self.request_queue_size = setting.REQUEST_QUEUE_SIZE
        self.download_queue_size = setting.DOWNLOAD_QUEUE_SIZE
        self.upload_queue_size = setting.UPLOAD_QUEUE_SIZE

    @staticmethod
    def request(seed: Seed) -> Union[Request, BaseItem]:
        yield Request(seed.url, seed, timeout=5)

    @staticmethod
    def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
        response = item.download()
        yield Response(item.seed, response, **item.to_dict)

    @staticmethod
    def parse(item: Response) -> BaseItem:
        upload_item = item.to_dict
        upload_item["text"] = item.response.text
        yield ConsoleItem(item.seed, data=json.dumps(upload_item, ensure_ascii=False))

    # @decorators.add_thread()
    @decorators.pause
    def build_request_item(self):
        thread_sleep = 0.1
        if TaskQueue.REQUEST.length >= self.request_queue_size:
            thread_sleep = 5
        elif seed := TaskQueue.TODO.pop():
            if seed.params.retry > self.spider_max_retries:
                seed.params.seed_status = DealModel.fail
            else:
                TaskQueue.process_task(seed, self.request)
            TaskQueue.DELETE.push(seed)
        time.sleep(thread_sleep)

    # @decorators.add_thread(num=setting.SPIDER_THREAD_NUM)
    @decorators.pause
    def build_download_item(self):
        thread_sleep = 0.1
        if TaskQueue.DOWNLOAD.length >= self.download_queue_size:
            logger.info(f"download queue is full, sleep {thread_sleep}s")
            thread_sleep = 5
        elif request_item := TaskQueue.REQUEST.pop():
            TaskQueue.process_task(request_item, self.download)
        time.sleep(thread_sleep)

    # @decorators.add_thread()
    @decorators.pause
    def build_parse_item(self):
        thread_sleep = 0.1
        if TaskQueue.UPLOAD.length >= self.upload_queue_size:
            logger.info(f"upload queue is full, sleep {thread_sleep}s")
            thread_sleep = 5
        if response_item := TaskQueue.RESPONSE.pop():
            TaskQueue.process_task(response_item, self.parse)
        time.sleep(thread_sleep)


