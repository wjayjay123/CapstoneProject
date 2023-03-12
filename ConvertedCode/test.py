import numpy as np
from tvi import tvi
import math
from quantizeNL_float import quantizeNL_float
from MaxQuart import maxQuart
from DCA_TMO import DCA_TMO

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

# a = [[10,20,30],[40,50,60],[70,80,90]]
# a = [[66.9567,7.4928,28.1919],[3.0966,90.4558,87.1903],[99.8430,60.6271,37.5480],[99.8430,60.6271,37.5480],[99.8430,60.6271,37.5480],[99.8430,60.6271,37.5480]]
# b = np.array(a)

# c = dCA_TMO(b)
# d = maxQuart(b.reshape(-1,1),0.99)
# e = maxQuart(b.reshape(-1,1),0.01)
# print(d,e)
# c,d,e = quantizeNL_float(b,3,b)
# print(c)
# print(d)
# print(e)

a = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
              [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
              [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])

b = DCA_TMO(a)