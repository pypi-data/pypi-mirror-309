import asyncio
import functools
from typing import Any, Callable, Coroutine


def concurrency_limit(max_concurrent_tasks: int) -> any:
    """
    限制最大并发任务数的装饰器

    :param max_concurrent_tasks: 最大并发任务数量
    :return: 包装后的函数
    """
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            async with semaphore:
                print(f"开始执行任务：{func.__name__}，参数：{args}, {kwargs}")
                result = await func(*args, **kwargs)
                print(f"完成任务：{func.__name__}，结果：{result}")
                return result

        return wrapper

    return decorator


# 使用示例
async def fetch_data(url: str) -> str:
    """
    模拟获取数据的异步函数

    :param url: 需要获取数据的URL地址
    :return: 获取到的数据
    """
    print(f"正在获取: {url}")
    await asyncio.sleep(1)  # 模拟 I/O 操作
    print(f"完成: {url}")
    return url


# 使用装饰器限制并发量，参数为最大并发任务数
@concurrency_limit(3)
async def limited_fetch_data(url: str) -> str:
    return await fetch_data(url)


# 模拟大量请求
async def main() -> None:
    urls = [f"http://example.com/{i}" for i in range(10)]
    tasks = [limited_fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print("所有任务完成:", results)


# 运行
asyncio.run(main())
