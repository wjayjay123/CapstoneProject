#Imports
import numpy as np

def quantizeNL_float(y, nclust, lum):

    lum = float(lum)
    lum0 = lum
    lum = np.reshape(lum, (1,lum.size))
    lum = np.sort(lum)