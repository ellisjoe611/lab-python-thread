import asyncio
from asyncio import AbstractEventLoop, Task
import time
from typing import Any


def do_sleep(sec, msg) -> str:
    time.sleep(sec)
    return msg

async def await_sync_function(func, *args, **kwargs) -> dict[str, Any]:
    res: Any = None
    try:
        event_loop: AbstractEventLoop = asyncio.get_running_loop()
        res = await event_loop.run_in_executor(None, func, *args, **kwargs)
        return {"status": 'fulfilled', "value": res}
    except RuntimeError as e:
        return {"status": 'rejected', "reason": str(e)}


async def main() -> None:
    tasks: list[Task] = []
    tasks.append(asyncio.create_task(await_sync_function(do_sleep, 2, "hello")))
    tasks.append(asyncio.create_task(await_sync_function(do_sleep, 4, "world")))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take aboud 2 seconds.)
    results: list[dict[str, Any]] = await asyncio.gather(*tasks)

    print(f"finished at {time.strftime('%X')}")
    print(results)

asyncio.run(main())
