import threading
import time
from typing import Optional
import queue

class thread_item:
    def __init__(self, func, args, manager, name:Optional[str]=None, description:Optional[str]=None):
        self.func = func
        self.args = args
        self.manager = manager

        self.thread = threading.Thread(target=self.job)

        self.name = name
        self.description = description
    
    def job(self):
        self.manager.processing_list.append(self)
        self.func(*self.args)
        self.manager.processing_list.remove(self)    

    def start(self):
        self.thread.start()

class func_item:
    def __init__(self, func, thread) -> None:
        self.func = func
        self.thread = thread

    def start(self, args:tuple = ()):
        # self.func(*args)
        self.thread.tasks.put((self.func, args))

class new_mq_thread:
    def __init__(self, manager, name:Optional[str]=None, description:Optional[str]=None):
        self.manager = manager
        self.tasks:queue.Queue[tuple[function, tuple]] = queue.Queue() # tasks: (func, args)
        self._stop = False
        threading.Thread(target=self.loop_thread, daemon=True).start()

        self.name = name
        self.description = description

    def loop_thread(self):
        while not self._stop:
            if not self.tasks.empty():
                task, args = self.tasks.get()
                task(*args)
            
                if not self.tasks.empty():
                    continue
            
            time.sleep(0.03)

    def add_func(self, func) -> func_item:
        return func_item(func, self)
    
    def run_func(self, func, args=()):
        self.tasks.put((func, args))

    def stop(self):
        self._stop = True


class thread_manager:
    def __init__(self):
        self.threads: list = []
        self.processing_list: list = []

    def add_func(self, func, args=(), name:Optional[str]=None, description:Optional[str]=None) -> thread_item:
        self.threads.append(thread := thread_item(func, args, self, name, description))
        return thread
    
    def add_thread(self, name:Optional[str]=None, description:Optional[str]=None) -> new_mq_thread:
        self.threads.append(thread := new_mq_thread(self, name, description))
        return thread
    
    def run_func(self, func, args=(), name:Optional[str]=None, description:Optional[str]=None):
        thread_item(func, args, self, name, description).start()
        print(self.threads)
        
    