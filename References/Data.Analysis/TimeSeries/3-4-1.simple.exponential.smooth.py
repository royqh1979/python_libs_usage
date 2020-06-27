import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

Motor = pd.read_csv("data/motororg.dat")

comp = Motor["complaints"]
comp.index = pd.date_range(start="1996",periods=len(comp),freq="M")

comp.plot()
#plt.show()

#拟合指数平滑模型
fit = SimpleExpSmoothing(comp).fit(smoothing_level=0.2,optimized=False)

print(fit.summary())

# 获取拟合值
# fitted = pd.Series(model.predict({'smoothing_level': 0.143, 'smoothing_slope': np.nan, 'smoothing_seasonal': np.nan, 'damping_slope': np.nan, 'initial_level': 17.7, 'initial_slope': np.nan, 'initial_seasons': np.array([], dtype=np.float64), 'use_boxcox': False, 'lamda': None, 'remove_bias': False},0,len(comp)-1))
# fitted.index = comp.index
fitted = fit.fittedvalues

#绘制拟合值
fitted.plot()


# 向后预测8期 (注意，simple exponential smooth的预测是“水平”的，
# 即拟合周期外的预测值y(h),y(h+1),y(h+2)...都相同

forecast=fit.predict(len(comp)+1,len(comp)+8)
#绘制预测结果
forecast.plot(style='--')
plt.show()