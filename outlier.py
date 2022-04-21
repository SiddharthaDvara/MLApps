import numpy as np
import pandas as pd





def detect_outliers(data):
    outlier=[]
    data=sorted(data)
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



