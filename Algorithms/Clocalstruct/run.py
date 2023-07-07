#this script details an example use of the LSEtools class

import time
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import math 
import matplotlib.pyplot as plt
import cv2 
from LSEtools import ClocalStruct as cs
from skimage.metrics import structural_similarity as ssim


path = "C:/Users/kiril/OneDrive/Documents/compvision_cw/VideoScaler/Test Results/Image Testing/Div2K0882/"

obj = cs("localStructV1", None, None, None, None)

img = cv2.imread(path+"0882x4.png")

gt = cv2.imread(path+"0882.png")

img = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB) 
gt = cv2.cvtColor(gt, cv2.COLOR_RGB2YCR_CB) 


imgx = img.shape[1]
imgy = img.shape[0]



t1 = time.time()
obj.resolve()
t2 = time.time()



res = obj.get_res()

plt.imshow(res)
plt.show()


#resp = res
obj2 = cs("localStructV1", res.shape[1], res.shape[0], 1, res)
t3 = time.time()
obj2.resolve()
t4 = time.time()


res = obj2.get_res()


print((t4-t3)+(t2-t1))

cv2.imwrite(path+"LSE2.png", res)

plt.imshow(res)
plt.show()

print(res.shape, gt.shape)
print(res.dtype, gt.dtype)

gtr = np.asarray(gt[5:-5,5:-5,0], dtype=np.uint8)


print(cv2.PSNR(res[5:-5, 5:-5], gtr))
print(ssim(res[5:-5, 5:-5], gt[5:-5,5:-5,0]))