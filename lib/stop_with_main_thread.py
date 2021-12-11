import ctypes
import inspect
import threading


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class StopWithMainThread:
    # 结果上看,这个类所理想的效果并未实现
    def __init__(self, func, if_join=False):
        self.thread = threading.Thread(target=func)
        self.thread.daemon = True
        self.if_join = if_join

    def run(self):
        self.thread.start()
        if self.if_join:
            self.thread.join()
