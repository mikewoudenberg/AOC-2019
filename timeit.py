import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        print('%r  %2.2f ms' %
              (method.__name__, (te - ts) * 1000))
        return result
    return timed
