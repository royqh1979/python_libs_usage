import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

CBE = pd.read_csv("data/cbe.dat",sep="\t")
CBE.index = pd.date_range(start="1958-01",periods=len(CBE),freq="M")
elec_ts = CBE["elec"]
beer_ts = CBE["beer"]
choc_ts = CBE["choc"]

model = seasonal_decompose(elec_ts,model="mul",period=12)
model.plot()
# fig,axis = plt.subplots(nrows=4,ncols=1,sharex=True)
# axis[0].plot(elec_ts.index, elec_ts)
# axis[0].set_ylabel("observed")
# axis[1].plot(elec_ts.index, model.trend)
# axis[1].set_ylabel("trend")
# axis[2].plot(elec_ts.index, model.seasonal)
# axis[2].set_ylabel("seasonal")
# axis[3].plot(elec_ts.index, model.resid)
# axis[3].set_ylabel("random")

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(elec_ts.index,model.trend*model.seasonal,linestyle="--")
ax.plot(elec_ts.index, model.trend )
plt.show()



