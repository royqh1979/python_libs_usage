# 使用hamoney季节模型拟合，以及如何选择合适的自变量
import numpy as np
import pandas as pd
import statsmodels.api as sm
import itertools
n=120
t=np.arange(1,n+1)
np.random.seed(1)
w=np.random.normal(0,0.5,n)
trend = 0.1+0.005*t+0.001*t**2
seasonal = np.sin(2*np.pi*t/12)+0.2*np.sin(2*np.pi*2*t/12)+0.1*np.sin(2*np.pi*4*t/12)+0.1*np.cos(2*np.pi*4*t/12)
sim = trend+seasonal+w

SIN = np.zeros((n,6))
COS = np.zeros((n,6))
for i in range(6):
    COS[:,i] = np.cos(2*np.pi*(i+1)*t/12)
    SIN[:,i] = np.sin(2*np.pi*(i+1)*t/12)
t2 = t**2
X = np.column_stack([t,t2,SIN,COS])
X = pd.DataFrame(X,columns=("Time","Time^2", "sin1", "sin2",
                            "sin3","sin4","sin5","sin6","cos1","cos2","cos3","cos4","cos5","cos6"))
# 使用全部变量进行拟合
X_const = sm.add_constant(X)
fit=sm.OLS(sim,X_const).fit()
print(fit.summary())
print("--------------------")
# stepwise model selections

best_fit = None
best_aic = None

predicators = list(X.columns)
# # 选择所有pvalue小于0.05（显著）的自变量
# predicators =[]
# for variable_name in fit.pvalues.index:
#     p = fit.pvalues[variable_name]
#     if p<0.05:
#         predicators.append(variable_name)
# print(predicators)

# 穷举这些变量的所有组合，找出AIC最小的
for k in range(1,len(predicators)+1):
    print(f" -- testing {k} variables ----")
    for variables in itertools.combinations(predicators,k):
        train_data = X[list(variables)]
        train_data = sm.add_constant(train_data)
        fit = sm.OLS(sim, train_data).fit()
        if best_aic is None or fit.aic < best_aic:
            print(f"Found a better model: {fit.aic} , {list(variables)}")
            best_aic = fit.aic
            best_fit = fit

print(best_fit.summary())
