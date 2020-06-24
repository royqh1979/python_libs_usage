import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读入1维列表(相当于R中的scan）
Global = np.loadtxt("data/global.dat")
Global = Global.ravel()
Global = pd.Series(Global)

Global.index = pd.date_range(start="1856",periods=len(Global),freq="M")
Global_annual = Global.resample("Y").mean()

fig,axis = plt.subplots(nrows=2,ncols=1,sharex=True)
Global.plot(ax=axis[0])
Global_annual.plot(ax=axis[1])

fig = plt.figure()
ax = fig.add_subplot()
New_series = Global[(Global.index.year>=1970) & (Global.index.year<=2005)]
# convert index to int64, to fit a trend line
New_time = New_series.index.astype(np.int64)
# fit trend line
z = np.polyfit(New_time,New_series,1)
p = np.poly1d(z)
np.poly1d
fit_values = p(New_time)
ax.plot(New_series.index, New_series)
ax.plot(New_series.index, fit_values)
plt.show()
