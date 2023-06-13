import asyncio
from asyncio import Task
import time
from concurrent.futures import ThreadPoolExecutor, Future


async def delayAsync(delay: int, msg: str) -> str:
    time.sleep(delay)
    print(msg)
    return msg


def delaySync(delay: int, msg: str) -> str:
    time.sleep(delay)
    print(msg)
    return msg


async def main_asyncio() -> None:
    print(f"started at {time.strftime('%X')}")

    task1: Task[str] = asyncio.create_task(delayAsync(1, "hello"))
    task2: Task[str] = asyncio.create_task(delayAsync(2, "world"))

    # Wait until both tasks are completed
    res: tuple[str, str] = await asyncio.gather(task1, task2)
    print(res)

    print(f"finished at {time.strftime('%X')}")


async def main_threadpool() -> None:
    print(f"started at {time.strftime('%X')}")
    # 기본 max_workers 갯수 : 5 ~ 32
    # max_workers = min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor() as executor:
        res1: Future[str] = executor.submit(delaySync, 1, "hello")
        res2: Future[str] = executor.submit(delaySync, 3, "y'all")
        res3: Future[str] = executor.submit(delaySync, 2, "and")
        res4: Future[str] = executor.submit(delaySync, 5, "the")
        res5: Future[str] = executor.submit(delaySync, 4, "world")
    print(f"finished at {time.strftime('%X')}")
    print((res1.result(), res2.result(), res3.result(), res4.result(), res5.result()))

if __name__ == "__main__":
    asyncio.run(main_threadpool())
