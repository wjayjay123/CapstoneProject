import numpy as np
from tvi import tvi
import math

a = [-3.95]

b = tvi(np.array(a))

c = tvi(np.array([-1.45]))

d = tvi(np.array([-0.0185]))

e = tvi(np.array([1.8]))

f = tvi(np.array([2]))

print(b,c,d,e,f)