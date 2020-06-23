import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CBE = pd.read_csv("data/cbe.dat",sep="\t")
CBE.index = pd.date_range(start="1958-01",periods=len(CBE),freq="M")
elec_ts = CBE["elec"]

AP = pd.read_csv("data\\airpassengers.csv")
AP=AP[["x"]]
AP.index = pd.date_range(start='1949-01', end='1961-01', freq='M')
# intersection = AP.index.intersection(elec_ts.index)
# AP_elec= pd.concat([AP[AP.index.isin(intersection)],elec_ts[elec_ts.index.isin(intersection)]],axis=1)

# 使用join操作对两个时间序列进行合并
AP_elec = AP.join(elec_ts, how="inner")

fig,axis = plt.subplots(nrows=2,ncols=1,sharex=True)

AP_elec.x.plot(ax=axis[0])
axis[0].set_ylabel("Air passengers / 1000's")
AP_elec.elec.plot(ax=axis[1])
axis[1].set_ylabel("Electricity production / MkWh")

fig=plt.figure()
ax = fig.add_subplot()
ax.scatter(AP_elec.x,AP_elec.elec)

# fit a trend line
z = np.polyfit(AP_elec.x,AP_elec.elec,1)
p = np.poly1d(z)
# draw the trend line
ax.plot(AP_elec.x, p(AP_elec.x))
plt.show()