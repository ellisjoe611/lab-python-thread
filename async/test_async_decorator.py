import asyncio
from asyncio import Task
import time
import os
import tracemalloc
from tracemalloc import StatisticDiff, Snapshot


def doCheckTime(func):
    def wrapper_sync(*args, **kwargs):
        start: float = time.time()
        res = func(*args, **kwargs)
        end: float = time.time()
        print(f'>>> 비동기 처리 총 소요 시간: {end - start}')
        return res

    async def wrapper_async(*args, **kwargs):
        start: float = time.time()
        res = await func(*args, **kwargs)
        end: float = time.time()
        print(f'>>> 비동기 처리 총 소요 시간: {end - start}')
        return res

    return wrapper_async if asyncio.iscoroutinefunction(func) else wrapper_sync


def checkTime(t: int):
    def decorator(func):
        async def wrapper_async(*args, **kwargs):
            print(f'>>> INPUT: {t}')
            start: float = time.time()
            res = await func(*args, **kwargs)
            end: float = time.time()
            print(f'>>> 비동기 처리 총 소요 시간: {end - start}')
            return res

        def wrapper_sync(*args, **kwargs):
            start: float = time.time()
            res = func(*args, **kwargs)
            end: float = time.time()
            print(f'>>> 동기 처리 총 소요 시간: {end - start}')
            return res

        return wrapper_async if asyncio.iscoroutinefunction(func) else wrapper_sync

    return decorator


async def main(n: int) -> int:
    await asyncio.sleep(n)
    print("[{0}] done".format(n))
    return n


@checkTime(43)
async def doit() -> list[int]:
    async_tasks: list[Task[int]] = [
        asyncio.create_task(main(4)),
        asyncio.create_task(main(2)),
        asyncio.create_task(main(1)),
        asyncio.create_task(main(5)),
        asyncio.create_task(main(3)),
        asyncio.create_task(main(7))
    ]

    res: list[int] = list()

    for i, task in enumerate(async_tasks):
        r: int = await task
        print("[{0}]th task is appended".format(i))
        res.append(r)

    return res


async def doitDir() -> None:
    tasks: list[Task[None]] = [
        asyncio.create_task(createDir(4)),
        asyncio.create_task(createDir(2)),
        asyncio.create_task(createDir(1)),
        asyncio.create_task(createDir(5)),
        asyncio.create_task(createDir(3)),
        asyncio.create_task(createDir(7)),
    ]
    await asyncio.gather(*tasks)


async def createDir(number: int) -> None:
    await asyncio.sleep(number)
    try:
        os.mkdir(f'./zzz_{str(number)}')
        print(f'created folder named zzz_{str(number)}')
    except:
        print(f'failed to create folder named zzz_{str(number)}')


async def doAsync() -> None:
    tracemalloc.start()
    snapshot1: Snapshot = tracemalloc.take_snapshot()

    print("BEGIN")
    res: tuple[list[int], list[int]] = await asyncio.gather(doit(), doit())
    # await doitDir()
    print("END")
    print(res)
    snapshot2: Snapshot = tracemalloc.take_snapshot()
    top_stats: list[StatisticDiff] = snapshot2.compare_to(snapshot1, 'lineno')

    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)

if __name__ == "__main__":
    asyncio.run(doAsync())
