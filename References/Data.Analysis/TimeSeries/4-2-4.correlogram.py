import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import acf
from statsmodels.graphics.tsaplots import plot_acf

w = np.random.normal(loc=0,scale=1000,size=1000)
print(acf(w,fft=False))
plot_acf(w)
plt.show()


