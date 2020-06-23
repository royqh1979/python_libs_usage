import pandas as pd
import matplotlib.pyplot as plt

CBE = pd.read_csv("data/cbe.dat",sep="\t")
CBE.index = pd.date_range(start="1958-01",periods=len(CBE),freq="M")
elec_ts = CBE["elec"]
beer_ts = CBE["beer"]
choc_ts = CBE["choc"]

fig, axes = plt.subplots(nrows=3,
                         ncols=1,
                         sharex=True)
elec_ts.plot(ax=axes[0])
axes[0].set_ylabel("Electricity")
beer_ts.plot(ax=axes[1])
axes[1].set_ylabel("Beer")
choc_ts.plot(ax=axes[2])
axes[2].set_ylabel("Chocolate")

plt.show()
