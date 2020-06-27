import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import statsmodels.graphics.api as tsp

aust = pd.read_csv("data/austourists.csv")
aust = aust["x"]
aust.index = pd.date_range(start="1999Q1",periods=len(aust),freq="Q")
print(aust.head())

aust =aust[aust.index.year>=2005]

model = ExponentialSmoothing(aust, seasonal_periods=4, trend="add",seasonal="add")
fit=model.fit(use_boxcox=True)
print(fit.summary())


fitted = fit.predict(start=0, end=len(aust) - 1)
forecast = fit.forecast(8)
aust.plot()
fitted.plot(color="orange")
forecast.plot(color="red",style="--")
plt.show()

