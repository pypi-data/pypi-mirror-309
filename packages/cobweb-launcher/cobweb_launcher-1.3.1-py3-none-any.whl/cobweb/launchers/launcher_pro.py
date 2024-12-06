import time

from base import TaskQueue, Decorators
from schedulers.scheduler_redis import RedisScheduler
from .launcher import Launcher


class LauncherPro(Launcher):

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__(task, project, custom_setting, **kwargs)
        self._redis_download = "{%s:%s}:download" % (project, task)
        self._redis_todo = "{%s:%s}:todo" % (project, task)
        self._scheduler = RedisScheduler(task, project)

    @Decorators.stop
    def _schedule(self):
        thread_sleep = self.scheduling_wait_time
        for q, key, size, item_info in [
            (TaskQueue.TODO, self._redis_todo, self.todo_queue_size, self._task_info["todo"]),
            (TaskQueue.DOWNLOAD, self._redis_download, self.download_queue_size, self._task_info["download"]),
        ]:
            if q.length < size:
                for member, priority in self._scheduler.schedule(
                    key, self.scheduling_size
                ):
                    q.push((member, priority), direct_insertion=True)
                    self.add_working_item(key.split(":")[-1], member, priority)
                thread_sleep = 0.1
        time.sleep(thread_sleep)

    @Decorators.pause
    def _heartbeat(self):
        if self._scheduler.working.is_set():
            self._scheduler.set_heartbeat()
        time.sleep(3)

    @Decorators.pause
    def _reset(self):
        self._scheduler.reset(
            keys=[self._redis_todo, self._redis_download],
            reset_time=self.seed_reset_seconds
        )
        time.sleep(30)

    @Decorators.pause
    def _insert(self):
        thread_sleep = 0.1
        for q, key, size in [
            (TaskQueue.SEED, self._redis_todo, self.seed_queue_size),
            (TaskQueue.REQUEST, self._redis_download, self.request_queue_size),
        ]:
            item_info = {}
            while item := q.pop() and len(item_info.keys()) < self.inserting_size:
                item_info[item.seed] = item.params.priority
            if q.length >= size:
                thread_sleep = self.inserting_wait_time
            self._scheduler.insert(key, item_info)
        time.sleep(thread_sleep)

    @Decorators.pause
    def _refresh(self):
        self._scheduler.refresh(self._redis_todo, self._task_info["todo"])
        self._scheduler.refresh(self._redis_download, self._task_info["download"])
        time.sleep(10)

    @Decorators.pause
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
