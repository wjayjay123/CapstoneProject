#Imports
import numpy as np
from scipy.interpolate import interp1d
import math
import statistics
import sys
from tvi import tvi

#Declare epsilon value
eps = sys.float_info[8]

def quantizeNL_float(y, nclust, lum):
    lum0 = lum
    lum = lum.flatten()
    lum = np.sort(lum)
    
    y = y.flatten()
    y = np.sort(y)

    edges = np.array([0, y.size])
    errors = np.sum(pow((y - np.mean(y)),2))
    errors = [errors]
    errors = np.array(errors)

    s_data = np.cumsum(y)
    ss_data = np.cumsum(pow(y,2))

    for i in range (1, nclust):
        idx = np.argmax(errors)
        k = edges[idx]
        n = edges[idx+1] - k

        sn = s_data[(k+n)-1]
        if(k >= 1):
            sn = sn - s_data[k-1]
        ssn = ss_data[(k+n)-1]
        if(k >= 1):
            ssn = ssn - ss_data[k-1]

        d = 2
        m = math.floor(n/d)

        while(1):
            sm = s_data[(k+m)-1]
            if(k >= 1):
                sm = sm - s_data[k-1]
            ssm = ss_data[(k+m)-1]
            if(k >= 1):
                ssm = ssm - ss_data[k-1]
            
            e1 = ssm - pow(sm,2)/m
            e2 = ssn - ssm - pow((sn - sm),2)/(n - m)
            d = 2 * d
            if(abs(e1-e2) < 0.001 or d >= n):
                lum1 = np.nanmedian(lum[k:k+m])
                lum2 = np.nanmedian(lum[k+m:k+n])
                delta1 = pow(10,tvi(math.log10(lum1)))
                delta2 = pow(10,tvi(math.log10(lum2)))
                temp = abs(delta1 / (delta1 + delta2) * (lum[(k+n-1)] - lum[k]) + lum[k] - lum[k:(k+n)])
                if temp.size == 0:
                    lum_loc = -1
                else:
                    lum_loc = np.nanargmin(abs(delta1 / (delta1 + delta2) * (lum[(k+n-1)] - lum[k]) + lum[k] - lum[k:(k+n)]))
                m = lum_loc + 1
                sm = s_data[(k+m)-1]
                if(k >= 1):
                    sm = sm - s_data[k-1]
                ssm = ss_data[(k+m)-1]
                if(k >= 1):
                    ssm = ssm - ss_data[k-1]
                e1 = ssm - pow(sm,2)/m
                e2 = ssn - ssm - pow((sn - sm),2) / (n - m)

                edges = np.concatenate((edges[:idx+1], np.array([k+m]), edges[idx+1:]))
                errors = np.concatenate((errors[:idx], np.array([e1, e2]), errors[idx+1:]))
                break
            else:
                if(e1 > e2):
                    m = m - math.floor(n/d);
                elif(e1 < e2):
                    m = m + math.floor(n/d);
    
    mdata = np.zeros(nclust)
    mdata[0] = np.min(lum0)
    mdata[-1] = np.max(lum0)

    for i in range(1, nclust-1):

        if lum[edges[i]-1]==lum[edges[i+1]-1]:
            ind = lum0[lum0==lum[edges[i]-1]]
            mdata[i] = np.mean(ind)+eps*i
        else:
            ind = lum0[(lum0 > lum[edges[i]-1]) & (lum0 <= lum[edges[i+1]-1])]
            mdata[i] = np.mean(ind)

    labels_mdata = np.linspace(1,256,num=nclust)
    interp = interp1d(mdata, labels_mdata, kind='linear')
    labels = interp(lum0)
    
    return labels, mdata, edges
