from . import api
import concurrent.futures

class ThreadManager(api.LeoRoutineAPI):
    def __init__(self) -> None:
        super().__init__()
        self.executor = concurrent.futures.ThreadPoolExecutor(thread_name_prefix="Thread")
        
    @api.start_logging
    def start_new_job(self, job, callback=None, **kwargs):
        def wrapped_job():
                result = job(**kwargs)
                if callback:
                    callback(result)
                return result

        
        # 提交任务到线程池
        future = self.executor.submit(wrapped_job)
        self.__routine__.append(future)
        
    @api.wait_logging
    def wait_all_jobs(self):
        # 等待所有已提交的任务完成
        for future in concurrent.futures.as_completed(self.__routine__):
            try:
                # 获取结果（这也会处理异常）
                future.result()
            except Exception as e:
                # 这里可以处理异常
                print(f"Job raised an exception: {e}")
        
        # 清空futures列表，因为所有工作都已完成
        self.__routine__.clear()
        
