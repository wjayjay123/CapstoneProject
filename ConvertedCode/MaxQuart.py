#Imports
import numpy as np

def maxQuart(matrix,percentile):
    if (percentile > 1.0):
        percentile = 1.0

    if (percentile < 0.0):
        percentile = 0.0
    
    [n, m] = matrix.shape
    matrix = np.sort(matrix.reshape(n * m, 1))
    index = round(n * m * percentile)
    index = max(index, 1)
    ret = matrix[index]
    return ret