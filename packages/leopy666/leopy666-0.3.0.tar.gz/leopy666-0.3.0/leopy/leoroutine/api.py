def start_logging(func):
    def wrapper(self, job, *args, **kwargs):
        # 打印新任务开始的信息，这里打印的是传入的 job 函数的名字
        print(f"开始新任务：{job.__name__}, args:= {args}, kwargs:= {kwargs}")
        return func(self, job, *args, **kwargs)
    return wrapper

def wait_logging(func):
    def wrapper(self, *args, **kwargs):
        print('等待所有jobs完成 ...')
        return func(self, *args, **kwargs)
    return wrapper

class LeoRoutineAPI:
    def __init__(self) -> None:
        self.__routine__ = []
    
    @start_logging
    def start_new_job(self, job,callback=None, **kwargs):
        # 实际的任务启动逻辑可以在这里实现
        raise NotImplementedError()
    
    @wait_logging
    def wait_all_jobs(self):
        # 等待所有任务完成的逻辑可以在这里实现
        raise NotImplementedError()

