import time

from nbody_cython import test_cython

def test(f,times=10):
    f()
    start = time.perf_counter_ns()
    for i in range(times):
        f()
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

if __name__ == "__main__":
    print("cython:")
    test(test_cython)