#this script details an example use of the LSEtools class

import time
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import math 
import matplotlib.pyplot as plt
import cv2 
from LSEtools import ClocalStruct as cs
import matplotlib.pyplot as plt

img = plt.imread("./Clocalstruct/im1.jpg")

imgx = img.shape[1]
imgy = img.shape[0]

obj = cs("localStructV1", imgx, imgy, 1, img)
obj.resolve()

res = obj.get_res()

plt.imshow(res)
plt.show()