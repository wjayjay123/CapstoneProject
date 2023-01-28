import cv2
import os
import DCA_TMO
import numpy

hdr_path = 'moto.hdr'

img = cv2.imread('moto.hdr', flags=cv2.IMREAD_ANYDEPTH)
print(img.shape)
dca = DCA_TMO.initialize()
test = dca.DCA_TMO(img)
result = numpy.array(test)
print(type(result))
cv2.imwrite("testimg.png", result)



# bytes = img.tobytes()
# print(type(bytes))
# print(bytes)
# result = cv2.imshow('test',img)
# path = os.getcwd()
# result = os.listdir(path)
# cv2.imshow('test',img)
# cv2.waitKey(0)