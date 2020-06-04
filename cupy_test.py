import numpy as np
import cupy as cp
import time

### Numpy and CPU
s = time.time()
x_cpu = np.random.uniform(0,1,(400,1000,1000))
e = time.time()
print(e - s)
### CuPy and GPU
s = time.time()
x_gpu = cp.random.uniform(0,1,(400,1000,1000))
e = time.time()
print(e - s)

### Numpy and CPU
s = time.time()
x_cpu *= 7
e = time.time()
print(e - s)
### CuPy and GPU
s = time.time()
x_gpu *= 7
e = time.time()
print(e - s)

### Numpy and CPU
s = time.time()
x_cpu *= 7
x_cpu *= x_cpu
x_cpu += x_cpu
e = time.time()
print(e - s)
### CuPy and GPU
s = time.time()
x_gpu *= 7
x_gpu *= x_gpu
x_gpu += x_gpu
e = time.time()
print(e - s)
