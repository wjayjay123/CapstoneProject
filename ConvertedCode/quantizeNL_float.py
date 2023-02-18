#Imports
import numpy as np
import math
import statistics
from tvi import tvi

def quantizeNL_float(y, nclust, lum):
    lum0 = lum
    lum = np.reshape(lum, (1,lum.size))
    lum = np.sort(lum)
    lum = lum[0]

    y = np.reshape(y, (1,y.size))
    y = np.sort(y)

    edges = [0, y.size]
    errors = np.sum(pow((y - np.mean(y)),2))
    errors = [errors,0]
    errors = np.array(errors)
    
    s_data = np.cumsum(y)
    ss_data = np.cumsum(pow(y,2))

    for i in range (0, nclust-1):
        idx = np.argmax(errors)
        k = edges[idx]
        n = edges[idx+1] - k
        sn = s_data[(k+n)-1]
        if(k >= 1):
            sn = sn - s_data[k]
        ssn = ss_data[(k+n)-1]
        if(k >= 1):
            ssn = ssn - ss_data[k]
        d = 2
        m = math.floor(n/d)
        i = 0
        while(i<1):
            sm = s_data[(k+m)-1]
            if(k >= 1):
                sm = sm - s_data[k]
            ssm = ss_data[(k+m)-1]
            if(k >= 1):
                ssm = ssm - ss_data[k]
            e1 = ssm - pow(sm,2)/m
            e2 = ssn - ssm - pow((sn - sm),2)/(n - m)
            d = 2 * d
            # if(abs(e1-e2) < 0.001 or d >= n):
            lum1 = statistics.median(lum[k:k+m])
            lum2 = statistics.median(lum[k+m:k+n])
            delta1 = pow(10,tvi(math.log10(lum1)))
            delta2 = pow(10,tvi(math.log10(lum2)))
            print(delta1,delta2)
            i+=1
