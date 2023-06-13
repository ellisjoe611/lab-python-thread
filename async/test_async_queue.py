import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # 대기열에서 "작업 항목"을 가져옵니다.
        sleep_for = await queue.get()

        # "sleep_for"초 동안 잠자기.
        await asyncio.sleep(sleep_for)

        # "작업 항목"이 처리되었음을 대기열에 알립니다.
        queue.task_done()

        print(f'{name} has slept for {sleep_for:.2f} seconds')


async def main():
    # "워크로드"를 저장하는 데 사용할 대기열을 만듭니다.
    queue = asyncio.Queue()

    # 무작위 타이밍을 생성하고 큐에 넣습니다.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # 대기열을 동시에 처리하기 위해 3 개의 작업자 작업을 만듭니다.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # 대기열이 완전히 처리 될 때까지 기다립니다.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # 작업자 작업을 취소합니다.
    for task in tasks:
        task.cancel()
    # 모든 작업자 작업이 취소 될 때까지 기다립니다.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


asyncio.run(main())
