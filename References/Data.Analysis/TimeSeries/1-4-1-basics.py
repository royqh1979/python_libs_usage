# 从数据文件中导入
import pandas as pd
import matplotlib.pyplot as plt

# 读入数据
data = pd.read_csv("data\\airpassengers.csv")
# 只保留x列
data=data[["x"]]
# 添加时间索引
# index = pd.Index(sm.tsa.datetools.dates_from_range("1949m1","1960m12"))
index = pd.date_range(start='1949-01', end='1961-01', freq='M')
data.index = index

# 聚集操作，计算年均值 和 半年标准差，注意resample使用
year_mean=data.resample("Y").mean()
half_year_std = data.resample("6M").std()
print(year_mean)
print(half_year_std)

# 用matplotlib画时序图
fig = plt.figure()
ax  = fig.add_subplot()
data.x.plot(ax=ax)
ax.set_ylabel("Passengers (1000's)")
#plt.show()

# 年度统计，注意resample使用
fig = plt.figure()
ax  = fig.add_subplot()
data.x.resample("Y").sum().plot(ax=ax)
#plt.show()

# 按月画箱图，注意groupby使用
fig = plt.figure()
ax  = fig.add_subplot()
data.groupby(lambda x:x.month).boxplot(ax=ax,subplots=False)
plt.show()

