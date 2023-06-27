
######################################################################################################################################################################
#imports:
#ctypes and ctypeslib allows python to work with, funnily enough c types.


from ctypes import *
import numpy as np
from numpy.ctypeslib import ndpointer
import math 
import matplotlib.pyplot as plt
import cv2

#####################################################################################################################################################################
#the shared library is imported into the python code
#the return and argument types are set


alg = cdll.LoadLibrary('./lib.so').alg
alg.restype = ndpointer(c_uint8, flags="C_CONTIGUOUS", shape = (128, 128))
alg.argtypes = [ndpointer(c_uint8, flags="C_CONTIGUOUS", shape = (64, 64)), c_uint16, c_uint16]


#####################################################################################################################################################################
#obtain test image by downloading imagenet and converting YCrBr

image = cv2.imread('test_1050.JPEG')
img = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

plt.imshow(img[:,:,0], cmap = 'gray')
#plt.show()
img = np.array(img[:,:,0], dtype = c_uint8)
#####################################################################################################################################################################
#Function with which to call the algorithm, the algorithm will split the image into 128x128 chunks so 
#the whole image can be kept in the L1 cache 


def SRwLocalStruct(img, xDim, yDim):

    return alg(img, xDim, yDim)



res = SRwLocalStruct(img, 64, 64)



plt.imshow(res, cmap = 'gray')
plt.show()















                

             




    