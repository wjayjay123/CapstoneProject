#Import
import cv2
import DCA_TMO
import numpy as np
import MaxQuart
import math

hdrPath = 'moto.hdr'

hdrImg = cv2.imread('moto.hdr', flags=cv2.IMREAD_ANYDEPTH)

# print(hdrImg.shape)
# print(hdrImg.reshape(-1,1).shape)

maxhdr = MaxQuart.maxQuart(hdrImg.reshape(-1,1),0.99)
minhdr = MaxQuart.maxQuart(hdrImg.reshape(-1,1),0.01)
# print(maxhdr)
# print(minhdr)

print(hdrImg[1,1,1])