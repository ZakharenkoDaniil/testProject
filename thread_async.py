from threading import Thread
from asyncio import sleep


class PlusThread(Thread):
    def __init__(self, a: int):
        super().__init__()
        self.__a = a
        self.__complete = False

    def get_a(self) -> int:
        return self.__a

    def is_complete(self):
        return self.__complete

    async def run(self) -> None:
        self.__a += 5
        await sleep(3)
        self.__a += 5
        await sleep(5)
        self.__complete = True

