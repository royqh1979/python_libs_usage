import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

Z=pd.read_csv("data/pounds_nz.dat",sep="\t")
Z.index = pd.date_range(start="1991Q1",periods=len(Z),freq="Q")

#绘制 趋势图
figure :Figure = plt.figure()
axis = figure.add_subplot()
Z["xrate"].plot(ax=axis)
axis.set_ylabel(" Quarterly exchange rate in $NZ / pound")
axis.set_xlabel(" Time(years) ")
# plt.show()

# 取部分时间段的数据
Z_92_96 = Z[ (1992<=Z.index.year) & (Z.index.year<1996)]
Z_96_98 = Z[ (1996<=Z.index.year) & (Z.index.year<1998)]

fig, axis = plt.subplots(nrows=2,ncols=1)
Z_92_96["xrate"].plot(ax=axis[0])
axis[0].set_ylabel(" Quarterly exchange rate in $NZ / pound")
axis[0].set_xlabel(" Time(years) ")
Z_96_98["xrate"].plot(ax=axis[1])
axis[1].set_ylabel(" Quarterly exchange rate in $NZ / pound")
axis[1].set_xlabel(" Time(years) ")
plt.show()



