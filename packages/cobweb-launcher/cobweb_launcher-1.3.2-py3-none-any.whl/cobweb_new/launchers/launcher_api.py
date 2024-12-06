import time
import threading

from cobweb.db import ApiDB
from cobweb.base import Seed, TaskQueue,logger, stop, pause
from cobweb.constant import DealModel
from .launcher import Launcher


class LauncherApi(Launcher):

    def __init__(self, task, project, custom_setting=None, **kwargs):
        super().__init__(task, project, custom_setting, **kwargs)
        self._db = ApiDB()

        self._todo_key = "{%s:%s}:todo" % (project, task)
        self._done_key = "{%s:%s}:done" % (project, task)
        self._fail_key = "{%s:%s}:fail" % (project, task)
        self._heartbeat_key = "heartbeat:%s_%s" % (project, task)

        self._statistics_done_key = "statistics:%s:%s:done" % (project, task)
        self._statistics_fail_key = "statistics:%s:%s:fail" % (project, task)
        self._speed_control_key = "speed_control:%s_%s" % (project, task)

        self._reset_lock_key = "lock:reset:%s_%s" % (project, task)

        self._heartbeat_start_event = threading.Event()

    @property
    def heartbeat(self):
        return self._db.exists(self._heartbeat_key)

    def statistics(self, key, count):
        if not self.task_model and not self._db.exists(key):
            self._db.setex(key, 86400 * 30, int(count))
        else:
            self._db.incrby(key, count)

    def _get_seed(self) -> Seed:
        """
        从队列中获取种子（频控）
        设置时间窗口为self._time_window（秒），判断在该窗口内的采集量是否满足阈值（self._spider_max_speed）
        :return: True -> 种子, False -> None
        """
        if TaskQueue.TODO.length and not self._db.auto_incr(
                self._speed_control_key, 
                t=self.time_window,
                limit=self.spider_max_count
        ):
            expire_time = self._db.ttl(self._speed_control_key)
            logger.info(f"Too fast! Please wait {expire_time} seconds...")
            time.sleep(expire_time / 2)
            return None
        return TaskQueue.TODO.pop()

    @stop
    def _reset(self):
        """
        检查过期种子，重新添加到redis缓存中
        """
        if self._db.lock(self._reset_lock_key, t=120):

            _min = -int(time.time()) + self.seed_reset_seconds \
                if self.heartbeat else "-inf"

            self._db.members(self._todo_key, 0, _min=_min, _max="(0")

            if not self.heartbeat:
                self._heartbeat_start_event.set()

            self._db.delete(self._reset_lock_key)

        time.sleep(30)

    @stop
    def _refresh(self):
        """
        刷新doing种子过期时间，防止reset重新消费
        """
        if self.doing_seeds:
            refresh_time = int(time.time())
            seeds = {k: -refresh_time - v / 1e3 for k, v in self.doing_seeds.items()}
            self._db.zadd(self._todo_key, item=seeds, xx=True)
        time.sleep(3)

    @stop
    def _scheduler(self):
        """
        调度任务，获取redis队列种子，同时添加到doing字典中
        """
        if not self._db.zcount(self._todo_key, 0, "(1000"):
            time.sleep(self.scheduler_wait_seconds)
        elif TaskQueue.TODO.length >= self.todo_queue_size:
            time.sleep(self.todo_queue_full_wait_seconds)
        else:
            members = self._db.members(
                self._todo_key, int(time.time()),
                count=self.todo_queue_size,
                _min=0, _max="(1000"
            )
            for member, priority in members:
                seed = Seed(member, priority=priority)
                TaskQueue.TODO.push(seed)
                self.doing_seeds[seed.to_string] = seed.params.priority

    @pause
    def _heartbeat(self):
        if self._heartbeat_start_event.is_set():
            self._db.setex(self._heartbeat_key, t=5)
        time.sleep(3)

    @pause
    def _insert(self):
        """
        添加新种子到redis队列中
        """
        seeds = {}
        for _ in range(self.new_queue_max_size):
            if seed := TaskQueue.SEED.pop():
                seeds[seed.to_string] = seed.params.priority
        if seeds:
            self._db.zadd(self._todo_key, seeds, nx=True)
        if TaskQueue.SEED.length < self.new_queue_max_size:
            time.sleep(self.new_queue_wait_seconds)

    @pause
    def _delete(self):
        """
        删除队列种子，根据状态添加至成功或失败队列，移除doing字典种子索引
        """
        seed_info = {"count": 0, "failed": [], "succeed": [], "common": []}
        status = TaskQueue.DONE.length < self.done_queue_max_size

        for _ in range(self.done_queue_max_size):
            seed = TaskQueue.DONE.pop()
            if not seed:
                break
            if seed.params.seed_status == DealModel.fail:
                seed_info["failed"].append(seed.to_string)
            elif self.done_model == 1:
                seed_info["succeed"].append(seed.to_string)
            else:
                seed_info["common"].append(seed.to_string)
            seed_info['count'] += 1

        if seed_info["count"]:

            succeed_count = int(self._db.zrem(self._todo_key, *seed_info["common"]) or 0)
            succeed_count += int(self._db.done([self._todo_key, self._done_key], *seed_info["succeed"]) or 0)
            failed_count = int(self._db.done([self._todo_key, self._fail_key], *seed_info["failed"]) or 0)

            if failed_count:
                self.statistics(self._statistics_fail_key, failed_count)
            if succeed_count:
                self.statistics(self._statistics_done_key, succeed_count)

            self._remove_doing_seeds(seed_info["common"] + seed_info["succeed"] + seed_info["failed"])

        if status:
            time.sleep(self.done_queue_wait_seconds)

