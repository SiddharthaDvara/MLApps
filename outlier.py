import numpy as np
import pandas as pd

#print(df['amount'])
sample= [15,101,18,7,13,16,11,21,5,15,10,9,-22]
#print(df)
#print("Original data")


outlier=[]
def detect_outliers(data):
    data=sorted(data)
    #print(data,len(data))
    q1=np.percentile(data,25)
    q3=np.percentile(data, 75)
    #print(q1,q3)
    IQR=q3-q1
    #print(IQR)
    lower=q1-(1.5*IQR)
    upper=q3+(1.5*IQR)
    #print(upper,lower)
    for i in data:
        if (i<lower or i>upper):
            outlier.append(i)


    return outlier

t=detect_outliers(df['amount'])
#print(t)
