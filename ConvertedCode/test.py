import numpy as np
from tvi import tvi
import math
from quantizeNL_float import quantizeNL_float

# a = [-3.95]

# b = tvi(np.array(a))

# c = tvi(np.array([-1.45]))

# d = tvi(np.array([-0.0185]))

# e = tvi(np.array([1.8]))

# f = tvi(np.array([2]))

# print(b,c,d,e,f)

# a = [[10,20,30],[40,50,60],[70,80,90]]
# b = np.array(a)
# print(b)
# b = pow(b,3)
# print(b)
# print(b.size)

a = [[10,20,30],[40,50,60],[70,80,90]];
b = np.array(a)
quantizeNL_float(b,55,b)