import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

t79=np.arange(1,11)
tdelt = np.arange(1,101)/10
sales = np.array([840,1470,2110,4000, 7590, 10950, 10530, 9470, 7790, 5890])
cusales = np.cumsum(sales)

# use non-linear least square to fit the BASS model
def bass_model(params,x):
    M=params[0]
    P=params[1]
    Q=params[2]
    return M * ( ((P+Q)**2 / P) * np.exp(-(P+Q) * x) ) / (1+(Q/P)*np.exp(-(P+Q)*x))**2

def bass_fun(params,x,y):
    return bass_model(params,x)-y

params0=[60530,0.03,0.38]
res = least_squares(bass_fun,params0,args=(t79,sales))
print(res)

# draw real sales
plt.scatter(t79,sales)
#plt.show()
# draw fitted sales
m,p,q=res.x
ngete = np.exp(-(p+q) * tdelt)
Bpdf = m * ( (p+q)**2 / p ) * ngete / (1 + (q/p) * ngete)**2
plt.plot(tdelt,Bpdf)
plt.show()


