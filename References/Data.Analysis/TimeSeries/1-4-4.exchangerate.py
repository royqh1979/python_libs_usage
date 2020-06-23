import pandas as pd
Z=pd.read_csv("data/pounds_nz.dat",sep="\t")
Z.index = pd.r
print(Z.head())