import julia
import time
start = time.perf_counter_ns()
jl  = julia.calc_julia(5000,(0.322+0.05j))
end = time.perf_counter_ns()
print(end-start)

start = time.perf_counter_ns()
jl  = julia.calc_julia_p(5000,(0.322+0.05j))
end = time.perf_counter_ns()
print(end-start)

import numpy as np
import matplotlib.pyplot as plt

plt.imshow(np.log(jl))
plt.show()