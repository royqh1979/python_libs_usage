import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# 产生10000个服从标准正态分布的随机数
w = np.random.standard_normal(10000)
figure = plt.figure()
plt.plot(w,linestyle="-")
#plt.show()


# 绘制直方图
figure = plt.figure()
plt.hist(w,bins=100, density=True)

# 绘制(-3,3)范围内的标准正态分布曲线
dist = st.norm(loc=0,scale=1)
x = np.linspace(-3,3,1000)
plt.plot(x, dist.pdf(x), color="red")
plt.show()
