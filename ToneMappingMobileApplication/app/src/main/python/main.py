#Import
import cv2
from DCA_TMO import DCA_TMO
import numpy as np
import MaxQuart
import math
import os
from os.path import dirname, join
from PIL import Image
import base64
import io
# from com.chaquo.python import Python

hdrPath = "moto.hdr"

# cv2.imwrite("test.png",ldrImg)

def main(data):
#     files_dir = str(Python.getPlatform().getApplication().getFilesDir())
    filename = join(dirname(__file__), "moto.hdr")
    tempInputFile = join(dirname(__file__),"temp.hdr")
#     tempInputArr = np.frombyte(data)
#     cv2.imwrite(tempInputFile,tempInputArr)
    hdrImg = cv2.imread(filename, flags=cv2.IMREAD_ANYDEPTH)
    ldrImg = DCA_TMO(hdrImg)
    saveFileName = join(dirname(__file__), "test.png")
    cv2.imwrite(saveFileName,ldrImg)
    testimg = cv2.imread(saveFileName, flags=cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.cvtColor(testimg,cv2.COLOR_BGR2RGB)
    pilImg = Image.fromarray(img_rgb)

    buff = io.BytesIO()
    pilImg.save(buff,format="PNG")
    imgStr = base64.b64encode(buff.getvalue())
    return "" + str(imgStr,'utf-8')
