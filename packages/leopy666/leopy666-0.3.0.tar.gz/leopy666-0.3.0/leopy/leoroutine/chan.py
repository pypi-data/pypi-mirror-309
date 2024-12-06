from asyncio import Queue

class Chan:
    def __init__(self, capacity=1):
        self._queue = Queue(maxsize=capacity)

    async def put(self, item):
        await self._queue.put(item)

    async def pop(self):
        return await self._queue.get()

    def empty(self):
        return self._queue.empty()

    def full(self):
        return self._queue.full()

    def size(self):
        return self._queue.qsize()


    