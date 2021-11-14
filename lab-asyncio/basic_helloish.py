import asyncio
from asyncio import tasks
from asyncio.events import AbstractEventLoop
from asyncio.tasks import Task
import time
from typing import Set


async def hi():
    print(f'{time.ctime()} Hi there!')
    await asyncio.sleep(1.0)                    # 타 코루틴을 실행
    print(f'{time.ctime()} Bye now!')

if __name__ == "__main__":
    # asyncio의 루프 인스턴스를 얻는다
    loop_hi: AbstractEventLoop = asyncio.get_event_loop()
    task_hi: Task = loop_hi.create_task(hi())
    loop_hi.run_until_complete(task_hi)

    tasks: Set[Task] = asyncio.all_tasks(loop=loop_hi)
    for task in tasks:
        task.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop_hi.run_until_complete(group)

    loop_hi.close()        # 루프의 모든 대기열을 비우고 executor를 종료
