import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.api import acf

wave = pd.read_csv("data/wave.dat")

print(acf(wave["waveht"],fft=False))

plt.figure()
wave["waveht"].plot()
plt.figure()
wave["waveht"][0:60].plot()

plot_acf(wave["waveht"])
plt.show()

