import time
import inspect
import threading
import importlib

from cobweb.constant import LogTemplate
from cobweb.utils import dynamic_load_class
from cobweb.base import TaskQueue, Decorators, logger
from cobweb import setting


class Launcher(threading.Thread):

    __CUSTOM_FUNC__ = {}

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__()
        self.task = task
        self.project = project
        self.custom_func = dict()
        self.app_time = int(time.time())

        self.check_emtpy_times = 0

        _setting = dict()

        if custom_setting:
            if isinstance(custom_setting, dict):
                _setting = custom_setting
            else:
                if isinstance(custom_setting, str):
                    custom_setting = importlib.import_module(custom_setting)
                if not inspect.ismodule(custom_setting):
                    raise Exception
                for k, v in custom_setting.__dict__.items():
                    if not k.startswith("__") and not inspect.ismodule(v):
                        _setting[k] = v

        _setting.update(**kwargs)

        for k, v in _setting.items():
            setattr(setting, k.upper(), v)

        self.before_scheduler_wait_seconds = setting.BEFORE_SCHEDULER_WAIT_SECONDS

        self.scheduling_wait_time = setting.SCHEDULING_WAIT_TIME
        self.inserting_wait_time = setting.INSERTING_WAIT_TIME
        self.removing_wait_time = setting.REMOVING_WAIT_TIME
        self.seed_reset_seconds = setting.SEED_RESET_SECONDS

        self.scheduling_size = setting.SCHEDULING_SIZE
        self.inserting_size = setting.INSERTING_SIZE
        self.removing_size = setting.REMOVING_SIZE

        self.todo_queue_size = setting.TODO_QUEUE_SIZE
        self.seed_queue_size = setting.SEED_QUEUE_SIZE
        self.request_queue_size = setting.REQUEST_QUEUE_SIZE
        self.download_queue_size = setting.DOWNLOAD_QUEUE_SIZE
        self.response_queue_size = setting.RESPONSE_QUEUE_SIZE
        self.upload_queue_size = setting.UPLOAD_QUEUE_SIZE
        self.delete_queue_size = setting.DELETE_QUEUE_SIZE
        self.done_queue_size = setting.DONE_QUEUE_SIZE

        self.spider_thread_num = setting.SPIDER_THREAD_NUM

        self.task_model = setting.TASK_MODEL

        self.stop = threading.Event()  # 结束事件
        self.pause = threading.Event()  # 暂停事件

        self.crawler_path = setting.CRAWLER
        self.pipeline_path = setting.PIPELINE

        self._threads = []

        self._task_info = dict(todo={}, download={})

    @property
    def request(self):
        """
        自定义request函数
        use case:
            from cobweb.base import Request, BaseItem
            @launcher.request
            def request(seed: Seed) -> Union[Request, BaseItem]:
                ...
                yield Request(seed.url, seed)
        """
        def decorator(func):
            self.custom_func['request'] = func
        return decorator

    @property
    def download(self):
        """
        自定义download函数
        use case:
            from cobweb.base import Request, Response, Seed, BaseItem
            @launcher.download
            def download(item: Request) -> Union[Seed, BaseItem, Response, str]:
                ...
                yield Response(item.seed, response)
        """
        def decorator(func):
            self.custom_func['download'] = func
        return decorator

    @property
    def parse(self):
        """
        自定义parse函数, xxxItem为自定义的存储数据类型
        use case:
            from cobweb.base import Request, Response
            @launcher.parse
            def parse(item: Response) -> BaseItem:
               ...
               yield xxxItem(seed, **kwargs)
        """
        def decorator(func):
            self.custom_func['parse'] = func
        return decorator

    def remove_working_items(self, key, items):
        for item in items:
            self._task_info[key].pop(item, None)

    def add_working_item(self, key, member, priority):
        self._task_info[key][member] = priority

    def check_alive(self):
        while not self.stop.is_set():
            if not self.pause.is_set():
                for thread in self._threads:
                    if not thread.is_alive():
                        thread.start()
            time.sleep(1)

    def _add_thread(self, func, num=1, obj=None, name=None, args=()):
        obj = obj or self
        name = obj.__class__.__name__ + name or func.__name__
        for i in range(num):
            func_name = name + "_" + str(i) if num > 1 else name
            self._threads.append(threading.Thread(name=func_name, target=func, args=(obj,) + args))

    @Decorators.stop
    def _polling(self):
        if TaskQueue.is_empty():
            if self.pause.is_set():
                run_time = int(time.time()) - self.app_time
                if not self.task_model and run_time > self.before_scheduler_wait_seconds:
                    logger.info("Done! ready to close thread...")
                    self.stop.set()
                else:
                    logger.info("pause! waiting for resume...")
            elif self.check_emtpy_times > 2:
                logger.info("pause! waiting for resume...")
                self.doing_seeds = {}
                self._task_info['todo'] = {}
                self._task_info['download'] = {}
                self.pause.set()
            else:
                logger.info(
                    "check whether the task is complete, "
                    f"reset times {3 - self.check_emtpy_times}"
                )
                self.check_emtpy_times += 1
        elif TaskQueue.TODO.length:
            logger.info(f"Recovery {self.task} task run！")
            self.check_emtpy_times = 0
            self.pause.clear()
        else:
            logger.info(LogTemplate.launcher_polling.format(
                task=self.task,
                memory_todo_count=len(self._task_info["todo"]),
                memory_download_count=len(self._task_info["download"]),
                todo_queue_len=TaskQueue.TODO.length,
                delete_queue_len=TaskQueue.DELETE.length,
                request_queue_len=TaskQueue.REQUEST.length,
                response_queue_len=TaskQueue.RESPONSE.length,
                done_queue_len=TaskQueue.DONE.length,
                upload_queue_len=TaskQueue.UPLOAD.length,
            ))
        time.sleep(10)

    def run(self):
        Crawler = dynamic_load_class(self.crawler_path)
        Pipeline = dynamic_load_class(self.pipeline_path)

        crawler = Crawler(pause=self.pause, custom_func=self.custom_func)
        pipeline = Pipeline(pause=self.pause)

        self._add_thread(obj=crawler, func=crawler.build_request_item)
        self._add_thread(obj=crawler, func=crawler.build_download_item, num=self.spider_thread_num)
        self._add_thread(obj=crawler, func=crawler.build_parse_item)
        self._add_thread(obj=pipeline, func=pipeline.run)

        self._add_thread(func=self._polling)

        self._init_schedule_thread()
        self.check_alive()

    def _init_schedule_thread(self):
        ...

