import asyncio
from asyncio.events import AbstractEventLoop
from asyncio.futures import Future
from asyncio.tasks import Task
import time
from typing import List, Tuple


async def hi(t: float = 1.0):
    print(f'{time.ctime()} Hi there! {t}')
    await asyncio.sleep(t % 4)                    # 타 코루틴을 실행
    print(f'{time.ctime()} Bye now! {t}')

    return True

if __name__ == "__main__":
    current_loop: AbstractEventLoop = asyncio.get_event_loop()

    tasks: List[Task] = [current_loop.create_task(hi(t)) for t in range(1, 10)]         # 실제로 실행할 coroutine 작업들을 task화하여 task 리스트에 모으기
    group_from_tasks: Future = asyncio.gather(*tasks)                                   # 모은 task 리스트를 그룹화하기
    results: Tuple[bool] = current_loop.run_until_complete(group_from_tasks)            # 생성된 그룹이 모두 끝날 때까지 실행하고나서 다음 코드를 실행하기

    current_loop.close()        # 루프 끝나면 종료하는지 잊지 말고!

    print(f"Finished.\n{results}")