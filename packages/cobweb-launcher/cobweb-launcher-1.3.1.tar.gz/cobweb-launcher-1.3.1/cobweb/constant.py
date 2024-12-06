
class CrawlerModel:

    default = "cobweb.crawlers.Crawler"
    file_air = "cobweb.crawlers.FileCrawlerAir"
    file_pro = "cobweb.crawlers.FileCrawlerPro"


class LauncherModel:
    task = "launcher model: task"
    resident = "launcher model: resident"


class DownloadModel:
    common = "download model: common"
    file = "download model: file"


class LogModel:
    simple = "log model: simple"
    common = "log model: common"
    detailed = "log model: detailed"


class DealModel:
    fail = "deal model: fail"
    done = "deal model: done"
    poll = "deal model: poll"


class LogTemplate:

    console_item = """
    ----------------------- start - console pipeline -----------------
            种子详情 \n{seed_detail}
            解析详情 \n{parse_detail}
    ----------------------- end  - console pipeline ------------------
    """

    launcher_polling = """
    ----------------------- start - 轮训日志: {task} -----------------
            正在运行任务
                构造请求任务数: {memory_todo_count}
                正在下载任务数: {memory_download_count}
            任务内存队列 
                待构造请求队列:  {todo_queue_len}
                待删除请求队列:  {delete_queue_len}
                待进行下载队列:  {request_queue_len}
                待解析响应队列:  {response_queue_len}
                待删除下载队列:  {done_queue_len}
            存储队列 
               待上传数据队列:  {upload_queue_len}
    ----------------------- end  - 轮训日志: {task} ------------------
    """

    launcher_air_polling = """
    ----------------------- start - 轮训日志: {task} -----------------
            内存队列 
                种子数:  {doing_len}
                待消费:  {todo_len}
                已消费:  {done_len}
            存储队列 
                待上传:  {upload_len}
    ----------------------- end  - 轮训日志: {task} ------------------
    """

    launcher_pro_polling = """
----------------------- start - 轮训日志: {task} -----------------
        内存队列 
            种子数:  {doing_len}
            待消费:  {todo_len}
            已消费:  {done_len}
        redis队列 
            种子数:  {redis_seed_count}
            待消费:  {redis_todo_len}
            消费中:  {redis_doing_len}
        存储队列 
            待上传:  {upload_len}
----------------------- end  - 轮训日志: {task} ------------------
"""

    download_exception = """
----------------------- download exception -----------------------
        种子详情 \n{detail}
        种子参数
            retry         :    {retry}
            priority      :    {priority}
            seed_version  :    {seed_version}
            identifier    :    {identifier}
        exception
            msg           :    {exception}
------------------------------------------------------------------
"""

    download_info = """
------------------------ download info ---------------------------
        种子详情 \n{detail}
        种子参数
            retry         :    {retry}
            priority      :    {priority}
            seed_version  :    {seed_version}
            identifier    :    {identifier}
        response 
            status        :    {status} \n{response}
------------------------------------------------------------------
"""

    @staticmethod
    def log_info(item: dict) -> str:
        return "\n".join([" " * 12 + f"{str(k).ljust(14)}:    {str(v)}" for k, v in item.items()])
