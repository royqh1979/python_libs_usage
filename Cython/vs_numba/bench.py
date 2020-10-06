import numpy as np
import time
from numba import jit
from pairwise import pairwise_cython


def pairwise_numpy(X):
    return np.sqrt(((X[:, None, :] - X) ** 2).sum(-1))

def pairwise_python(X):
    M = X.shape[0]
    N = X.shape[1]
    D = np.empty((M, M), dtype=np.float)
    for i in range(M):
        for j in range(M):
            d = 0.0
            for k in range(N):
                tmp = X[i, k] - X[j, k]
                d += tmp * tmp
            D[i, j] = np.sqrt(d)
    return D

def test(f,times=10):
    X = np.random.random((200, 200))
    result=f(X)
    start = time.perf_counter_ns()
    for i in range(times):
        X = np.random.random((200,200))
        result = f(X)
    end = time.perf_counter_ns()
    ave_time = (end-start)/times
    if ave_time < 10000:
        print(f"{ave_time:.2f}ns per loop")
    elif ave_time < 1000000:
        print(f"{ave_time/1000:.2f}us per loop")
    elif ave_time < 1000000000:
        print(f"{ave_time/1000000:.2f}ms per loop")
    else:
        print(f"{ave_time/1000000000:.2f}s per loop")

pairwise_numba = jit(pairwise_python)

# print("PYTHON")
# test(pairwise_python)
print("#NUMPY")
test(pairwise_numpy)

# PYTHON
# 5.41s per loop
# #NUMPY
# 51.78ms per loop
print("Numba")
test(pairwise_numba)
print("Cython")
test(pairwise_cython)

