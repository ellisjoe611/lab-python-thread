import asyncio
import time


async def hi(t: float = 1.0):
    print(f'{time.ctime()} Hi there! {t}')
    await asyncio.sleep(t)                    # 타 코루틴을 실행
    print(f'{time.ctime()} Bye now! {t}')

if __name__ == "__main__":
    print("running...")
    asyncio.run(hi(5.0))                           # 해당 async def 함수를 실행
    asyncio.run(hi())                           # 해당 async def 함수를 실행
    asyncio.run(hi(3.0))                           # 해당 async def 함수를 실행
    print("done")
