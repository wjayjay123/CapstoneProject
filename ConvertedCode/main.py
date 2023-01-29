#Import
import cv2
import DCA_TMO
import numpy as np
import MaxQuart
import math

hdrPath = 'moto.hdr'

hdrImg = cv2.imread('moto.hdr', flags=cv2.IMREAD_ANYDEPTH)

testarr = np.array([[13],[34],[31],[65],[19],[68]])
print(testarr.shape)
# maxhdr = MaxQuart.maxQuart(hdrImg.reshape(-1,1),0.99)
# minhdr = MaxQuart.maxQuart(hdrImg.reshape(-1,1),0.01)

maxhdr = MaxQuart.maxQuart(testarr,0.99)
minhdr = MaxQuart.maxQuart(testarr,0.01)

print(maxhdr)
print(minhdr)