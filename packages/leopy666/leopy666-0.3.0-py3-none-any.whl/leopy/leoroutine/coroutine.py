import asyncio
from typing import Coroutine
from . import api

class CoroutineManager(api.LeoRoutineAPI):
    def __init__(self) -> None:
        super().__init__()
        self.__routine__ = []

    @api.start_logging
    def start_new_job(self, job: Coroutine, callback = None, **kwargs):
        # 创建一个包装后的协程函数，以便在完成后调用回调
        async def wrapped_job():
            try:
                result = await job(**kwargs)
                if callback:
                    callback(result)
                return result
            except Exception as e:
                if callback:
                    callback(None, exception=e)
                raise  # Re-raise the exception to be handled in wait_all_jobs

        # 创建并安排协程任务
        task = asyncio.create_task(wrapped_job())
        self.__routine__.append(task)

    @api.wait_logging
    async def wait_all_jobs(self):
        # 等待所有已提交的任务完成
        results = await asyncio.gather(*self.__routine__, return_exceptions=True)
        
        # 处理可能抛出的异常
        for result in results:
            if isinstance(result, Exception):
                print(f"Job raised an exception: {result}")
        
        # 清空任务列表，因为所有工作都已完成
        self.__routine__.clear()