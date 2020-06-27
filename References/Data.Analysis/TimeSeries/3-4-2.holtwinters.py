import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import statsmodels.graphics.api as tsp

wine = pd.read_csv("data/wine.dat",sep="\t")
print(wine.head())
sweetw = wine["sweetw"]
sweetw.index = pd.date_range(start="1980-01",periods=len(sweetw),freq="M")

sweetw.plot()
# plt.show()

model = ExponentialSmoothing(sweetw, seasonal_periods=12, trend="add",seasonal="mul")
fit=model.fit(use_boxcox=True,use_brute=True)
print(fit.summary())
print(fit.sse / len(sweetw))

plt.show()

