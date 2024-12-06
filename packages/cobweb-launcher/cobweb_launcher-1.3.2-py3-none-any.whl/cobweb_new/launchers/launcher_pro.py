import time

from base import TaskQueue
from cobweb.base import decorators
from schedulers.scheduler_redis import RedisScheduler
from .launcher import Launcher


class LauncherPro(Launcher):

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__(task, project, custom_setting, **kwargs)
        self._redis_download = "{%s:%s}:download" % (project, task)
        self._redis_todo = "{%s:%s}:todo" % (project, task)
        self._scheduler = RedisScheduler(task, project)

    # @decorators.add_thread()
    @decorators.stop
    def _schedule(self):
        thread_sleep = self.scheduling_wait_time
        for q, key, size in [
            (TaskQueue.TODO, self._redis_todo, self.todo_queue_size),
            (TaskQueue.DOWNLOAD, self._redis_download, self.download_queue_size),
        ]:
            if q.length < size:
                for item in self._scheduler.schedule(
                    key, self.scheduling_size
                ):
                    q.push(item)
                thread_sleep = 0.1
        time.sleep(thread_sleep)

    # @decorators.add_thread()
    @decorators.pause
    def _heartbeat(self):
        if self._scheduler.working.is_set():
            self._scheduler.set_heartbeat()
        time.sleep(3)

    # @decorators.add_thread()
    @decorators.pause
    def _reset(self):
        self._scheduler.reset(
            keys=[self._redis_todo, self._redis_download],
            reset_time=self.seed_reset_seconds
        )
        time.sleep(15)

    # @decorators.add_thread()
    @decorators.pause
    def _insert(self):
        thread_sleep = 0.1
        for q, key, size in [
            (TaskQueue.SEED, self._redis_todo, self.seed_queue_size),
            (TaskQueue.REQUEST, self._redis_download, self.request_queue_size),
        ]:
            items = {}
            while item := q.pop() and len(items.keys()) < self.inserting_size:
                items[item.to_string] = item.params.priority
            if q.length >= size:
                thread_sleep = self.inserting_wait_time
            self._scheduler.insert(key, items)
        time.sleep(thread_sleep)

    # @decorators.add_thread()
    @decorators.pause
    def _refresh(self):
        self._scheduler.refresh(self._redis_todo, self._task_info["todo"])
        self._scheduler.refresh(self._redis_download, self._task_info["download"])
        time.sleep(3)

    # @decorators.add_thread()
    @decorators.pause
    def _remove(self):
        thread_sleep = self.removing_wait_time
        for q, key, size in [
            (TaskQueue.DELETE, self._redis_todo, self.delete_queue_size),
            (TaskQueue.DONE, self._redis_download, self.done_queue_size),
        ]:
            items = []
            while item := q.pop() and len(items) < self.removing_size:
                items.append(item)
            self._scheduler.delete(key, *items)
            self.remove_working_items(key.split(":")[-1], items)
            if q.length >= size:
                thread_sleep = 0.1
        time.sleep(thread_sleep)

    def _init_schedule_thread(self):
        self._add_thread(func=self._heartbeat)
        self._add_thread(func=self._reset)
        self._add_thread(func=self._refresh)
        self._add_thread(func=self._schedule)
        self._add_thread(func=self._insert)
        self._add_thread(func=self._remove)
        self._add_thread(func=self._polling)
