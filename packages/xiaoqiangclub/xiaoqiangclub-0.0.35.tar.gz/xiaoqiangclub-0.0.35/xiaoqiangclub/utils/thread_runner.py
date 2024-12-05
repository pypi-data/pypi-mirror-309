# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/12 07:12
# 文件名称： thread_runner.py
# 项目描述： 在单独线程中运行指定的函数
# 开发工具： PyCharm
from queue import Queue
from threading import Thread
from typing import Callable, Any, Tuple, Optional
from xiaoqiangclub.config.log_config import log


def run_in_thread(func: Callable[..., Any], return_result: bool = False,
                  daemon: bool = False, *args: Any, **kwargs: Any) -> Tuple[Thread, Optional[Queue]]:
    """
    在单独线程中运行指定的函数，并根据需要返回线程和队列以获取返回值
    获取结果：
    ret = result_queue.get() if result_queue else None   # 阻塞式获取结果
    ret = result_queue.get_nowait() if result_queue else None   # 非阻塞式获取结果，请使用try-except语句处理异常，get_nowait()方法可能会导致程序崩溃。

    :param func: 需要在线程中运行的函数
    :param return_result: 是否需要返回结果队列
    :param daemon: 是否将线程设置为守护线程（和主线程一起退出），默认为False：主程序退出时，主线程会等待所有非守护线程完成后才会终止。True：主程序退出时，守护线程会被自动终止，无论它是否已经完成。
    :param args: 函数的参数
    :param kwargs: 函数的关键字参数
    :return: 包含线程和可选队列的元组
    """

    result_queue = Queue() if return_result else None

    def thread_target():
        log.info(f"{func.__name__} 线程启动...")
        try:
            result = func(*args, **kwargs)
            if return_result:
                result_queue.put(result)
            log.info(f"{func.__name__} 执行结束！")
        except Exception as e:
            log.error(f"{func.__name__} 线程执行出错！", exc_info=True)
            if return_result:
                result_queue.put(e)

    thread = Thread(target=thread_target)
    thread.daemon = daemon  # 将线程设置为守护线程
    thread.start()
    return thread, result_queue
