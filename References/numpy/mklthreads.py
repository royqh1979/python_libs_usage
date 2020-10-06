## Set maximum thread num used by MKL
import ctypes

class MKLThreads(object):
    _mkl_rt = None

    @classmethod
    def _mkl(cls):
        if cls._mkl_rt is None:
            try:
                cls._mkl_rt = ctypes.CDLL('libmkl_rt.so')
            except OSError:
                cls._mkl_rt = ctypes.CDLL('mkl_rt.dll')
        return cls._mkl_rt

    @classmethod
    def get_max_threads(cls):
        return cls._mkl().mkl_get_max_threads()

    @classmethod
    def set_num_threads(cls, n):
        assert type(n) == int
        cls._mkl().mkl_set_num_threads(ctypes.byref(ctypes.c_int(n)))

    def __init__(self, num_threads):
        self._n = num_threads
        self._saved_n = self.get_max_threads()

    def __enter__(self):
        self.set_num_threads(self._n)
        return self

    def __exit__(self, type, value, traceback):
        self.set_num_threads(self._saved_n)
