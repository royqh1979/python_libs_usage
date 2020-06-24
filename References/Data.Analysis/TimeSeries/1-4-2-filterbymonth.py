import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#读入数据
maine_month = pd.read_csv("data/Maine.dat")

maine_month.index = pd.date_range(start="1996-01",periods=len(maine_month),freq="M")
maine_annual = maine_month.resample("Y").mean()

# 计算二月和八月平均失业率 和 总平均失业率的比值
# 注意如何选取2月和8月的数据
maine_feb=maine_month[maine_month.index.month==2].unemploy
maine_aug=maine_month[maine_month.index.month==8].unemploy

feb_ratio = np.mean(maine_feb) / np.mean(maine_month.unemploy)
aug_ratio = np.mean(maine_aug) / np.mean(maine_month.unemploy)
print(np.mean(maine_feb), np.mean(maine_aug), np.mean(maine_month.unemploy))
print(f"{feb_ratio:.3f}, {aug_ratio:.3f}")


#绘制图形
ax1=plt.subplot(2,1,1)
maine_month.plot(ax=ax1)
ax1.set_ylabel("unemployed (%)")

ax2=plt.subplot(2,1,2)
maine_annual.plot(ax=ax2)
ax2.set_ylabel("unemployed (%)")
plt.show()