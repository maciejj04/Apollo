from functools import wraps
import threading

def executeInNewThread(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        import random
        func_hl = threading.Thread(name="notify_thread:{}".format(random.randint(0, 9999)), target=func, args=args,
                                   kwargs=kwargs)
        func_hl.start()
        return func_hl
    
    return async_func