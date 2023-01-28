import cv2
import numpy
import DCA_TMO
from os.path import dirname, join


def main():

    try:
        filename = join(dirname(__file__), "moto.hdr")
        hdr = cv2.imread(filename, flags=cv2.IMREAD_ANYDEPTH)
        hdrtoldr = DCA_TMO.initialize()
        ldr = hdrtoldr.DCA_TMO(hdr)
        ldrImg = numpy.array(ldr)
        cv2.imwrite("testimg.png", ldrImg)
        return "pass"
    except:
        return "fail"