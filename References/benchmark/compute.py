import numpy as np
import cupy as cp
import time
ee = int(1e8)
np.random.seed(6)
A = np.random.random(size=[ee,])
B = np.random.random(size=[ee,])
start = time.perf_counter()
c1 = np.dot(A,B)
end = time.perf_counter()
print('numpy C :',c1)
print('numpy time : /s',end-start)

A2 = cp.random.random(size=[ee,])
B2 = cp.random.random(size=[ee,])
start = time.perf_counter()
c2 = cp.dot(A2,B2)
end = time.perf_counter()
print('cupy C :',c2)
print('cupy time : /s',end-start)


start = time.perf_counter()
C = 0
for i in range(ee):
    C = C + A[i]*B[i]
end = time.perf_counter()
print('CPU C :',C)
print('CPU TIME : /s',end-start)
