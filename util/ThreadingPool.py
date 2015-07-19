
from Queue import Queue, Empty
from threading import Thread


class Worker(Thread):

    def __init__(self, thread_pool, **kargs):
        Thread.__init__(self)
        self.thread_pool = thread_pool
        self.setDaemon(True)
        self.is_stop = False
        self.start()

    def run(self):
        while True:
            if self.is_stop == True:
                break
            try :
                func, args, kargs = self.thread_pool.work_queue.get()
            except Empty:
                continue
            try:
                res = func(*args, **kargs)
                self.thread_pool.result_queue.put(res)
                self.thread_pool.job_done()
            except:
                break

    def stop(self):
        self.is_stop = True


class ThreadPool:

    def __init__(self, thread_num = 100):
        self.work_queue = Queue()
        self.result_queue = Queue()
        self.thread_pool = []
        self.thread_num = thread_num

    def start_threads(self):
        for i in range(self.thread_num):
            self.thread_pool.append(Worker(self))

    def wait_for_complete(self):
        self.work_queue.join()

    def add_job(self, callable, *args, **kargs):
        self.work_queue.put((callable, args, kargs))

    def job_done(self):
        self.work_queue.task_done()

    def get_result(self, *args, **kargs):
        return self.result_queue.get(*args, **kargs)

    def has_next_result(self):
        return not self.result_queue.empty()

    def stop_threads(self):
        for thread in self.thread_pool:
            thread.stop()
        del self.thread_pool[:]

