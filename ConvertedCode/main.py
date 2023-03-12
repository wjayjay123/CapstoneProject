#Import
import cv2
from DCA_TMO import DCA_TMO
import numpy as np
import MaxQuart
import math

hdrPath = 'moto.hdr'

hdrImg = cv2.imread('moto.hdr', flags=cv2.IMREAD_ANYDEPTH)

a = DCA_TMO(hdrImg)

# maxhdr = MaxQuart.maxQuart(testarr,0.99)
# minhdr = MaxQuart.maxQuart(testarr,0.01)