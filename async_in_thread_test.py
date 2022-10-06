import asyncio


async def plus_20(a: int) -> int:
    await asyncio.sleep(20)
    print(a+20)
    return a+20


async def plus_10(a: int) -> int:
    await asyncio.sleep(10)
    print(a+10)
    return a+10


async def main():
    a = 10
    task1 = asyncio.create_task(plus_20(a))
    task2 = asyncio.create_task(plus_10(a))



asyncio.run(main())
