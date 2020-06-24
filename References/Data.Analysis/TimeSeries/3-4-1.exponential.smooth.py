import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

Motor = pd.read_csv("data/motororg.dat")

comp = Motor["complaints"]
comp.index = pd.date_range(start="1996",periods=len(comp),freq="M")

comp.plot()
#plt.show()

#拟合指数平滑模型
model = SimpleExpSmoothing(comp)
model.fit()
print(model.params)
values=(list(comp))

# 使用拟合的模型预测
predictions = pd.Series(model.predict(model.params, start=0, end=len(comp) - 1))
predictions.index = comp.index
sse = sum((predictions) - values)

predictions.plot()
plt.show()