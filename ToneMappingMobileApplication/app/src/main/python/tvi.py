#Imports
import numpy as np

def tvi(intensity):
    intensity = np.array([intensity])
    threshold = np.zeros(intensity.shape)

    idx = np.where(intensity < -3.94)
    threshold[idx] = -2.86
    
    idx = np.where(intensity >= -3.94 and intensity < -1.44)
    threshold[idx] = pow((0.405 * intensity[idx] + 1.6), (2.18)) - 2.86

    idx = np.where(intensity >= -1.44 and intensity < -0.0184)
    threshold[idx] = intensity[idx] - 0.395

    idx = np.where(intensity >= -0.0184 and intensity < 1.9)
    threshold[idx] = pow((0.249 * intensity[idx] + 0.65) , (2.7)) - 0.72

    idx = np.where(intensity >= 1.9)
    threshold[idx] = intensity[idx] - 1.255;

    threshold = threshold - 0.95

    return threshold