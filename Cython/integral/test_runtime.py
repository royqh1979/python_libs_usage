from Cython.integral.integ import integrate_f
import time


f = lambda x: x**2-x

def py_inte(a, b, N):
    s = 0
    dx = (b-a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx


if __name__ == '__main__':
    start = time.perf_counter()
    for k in range(1000):
        py_inte(-10, 10, 1000)
    print('pure python takes {}'.format(time.perf_counter() - start))

    start = time.perf_counter()
    for k in range(1000):
        integrate_f(-10, 10, 1000)
    print('cython takes {}'.format(time.perf_counter() - start))
