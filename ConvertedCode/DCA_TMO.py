#Imports
from MaxQuart import maxQuart
from quantizeNL_float import quantizeNL_float
from matlabGauss import fspecial_gauss
from scipy.ndimage import convolve
import numpy as np

def DCA_TMO(hdrImg):
    K = 55

    maxhdr = maxQuart(hdrImg.reshape(-1,1),0.99)
    minhdr = maxQuart(hdrImg.reshape(-1,1),0.01)
    hdrImg[hdrImg > maxhdr] = maxhdr
    hdrImg[hdrImg < minhdr] = minhdr

    hdrLum = 0.2126 * hdrImg[:,:,0] + 0.7152 * hdrImg[:,:,1] + 0.0722 * hdrImg[:,:,2]
    hdrLum1 = hdrLum / max((hdrImg.reshape(-1,1)))
    hdrPQ = pow(((107 / 128 + 2413/128 * pow(hdrLum1,(1305/8192)))) / (1 + 2392 / 128 * pow(hdrLum1,(1305/8192))),(2523/32))
    labels,temp,temp1 = quantizeNL_float(hdrPQ, K, hdrLum)

    #For easier value checking
    # np.set_printoptions(precision=5, suppress=True)
    # a = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    #           [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
    #           [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
    # labels = a

    sigmaC = 0.5
    sigmaS = 0.8
    window = 9
    gfilterC = fspecial_gauss(window,sigmaC)
    gfilterS = fspecial_gauss(window,sigmaS)
    DoGfilter = gfilterC - gfilterS
    hdrPQnor = 255 * (hdrPQ - min(hdrPQ.reshape(-1,1))) / (max(hdrPQ.reshape(-1,1)) - min(hdrPQ.reshape(-1,1))) + 1
    tempLabel = labels * 0.65
    tempLabel[:,:,0] = tempLabel[:,:,0] + hdrPQnor * 0.35
    tempLabel[:,:,1] = tempLabel[:,:,1] + hdrPQnor * 0.35
    tempLabel[:,:,2] = tempLabel[:,:,2] + hdrPQnor * 0.35
    hdrPQnor = tempLabel
    tempConv = hdrPQnor
    tempConv[:,:,0] = convolve(hdrPQnor[:, :, 0], DoGfilter, mode='nearest')
    tempConv[:,:,1] = convolve(hdrPQnor[:, :, 1], DoGfilter, mode='nearest')
    tempConv[:,:,2] = convolve(hdrPQnor[:, :, 2], DoGfilter, mode='nearest')
    labels_DoG = labels + 3.0*tempConv
    s1 = (labels_DoG - min(labels_DoG.reshape(-1,1))) / (max(labels_DoG.reshape(-1,1)) - min(labels_DoG.reshape(-1,1)))
    s = 1 - np.arctan(s1)
    s = np.minimum(s, 0.5)
    tempHdrImg = hdrImg.astype(float)
    tempHdrImg[:,:,0] = tempHdrImg[:,:,0] / hdrLum
    tempHdrImg[:,:,1] = tempHdrImg[:,:,1] / hdrLum
    tempHdrImg[:,:,2] = tempHdrImg[:,:,2] / hdrLum
    ldrImg_DoG = pow(tempHdrImg,s) * labels_DoG
    maxx = maxQuart(ldrImg_DoG.reshape(-1,1),0.99)
    minn = maxQuart(ldrImg_DoG.reshape(-1,1),0.01)
    if (maxx < 255):
        if (max(ldrImg_DoG.reshape(-1,1)) < 255):
            maxx = max(ldrImg_DoG.reshape(-1,1))
        else:
            maxx = 255
    if (minn > 0):
        if (min(ldrImg_DoG.reshape(-1,1)) > 0):
            minn = min(ldrImg_DoG.reshape(-1,1))
        else:
            minn = 0
    ldrImg_DoG[ldrImg_DoG > maxx] = maxx
    ldrImg_DoG[ldrImg_DoG < minn] = minn
    tempLdrImg = ldrImg_DoG - minn
    tempLdrImg[:,:,0] = tempLdrImg[:,:,0] / (maxx-minn)
    tempLdrImg[:,:,1] = tempLdrImg[:,:,1] / (maxx-minn)
    tempLdrImg[:,:,2] = tempLdrImg[:,:,2] / (maxx-minn)
    ldrImg = 255 * tempLdrImg
    return ldrImg
    
   

