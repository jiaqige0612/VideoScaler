#This script implements all necessary tools to super-resolve images and video using the
#local structure estimation methods V1, V2 and V3 as detailed in the documentation.



import time
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import math 
import matplotlib.pyplot as plt
import cv2 

class ClocalStruct(object):

  def __init__(self, method, xDim, yDim, frames=1,  img=None):


    self.xDim = xDim
    self.yDim = yDim
    self.frames = frames

    self.img = img

    #set dimension parameters to pass into C libraries
    xDim = img.shape[1]
    yDim = img.shape[0]

    #setup C libraries
    self.lib = ctypes.cdll.LoadLibrary('./Clocalstruct/lib/{}.so'.format(method))

    self.alg = self.lib.alg

    self.alg.argtypes = [ndpointer(ctypes.c_uint8, flags="C_CONTIGUOUS"), ndpointer(ctypes.c_uint8, flags = "C_CONTIGUOUS"), ctypes.c_uint32, ctypes.c_uint32]

    #initialise result array
    self.res = np.empty(shape = (frames, yDim*2, self.xDim*2, 3), dtype = int)

    



  def exe(self, frame):

    #declare ctypes result arrays
    resR = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)
    resG = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)
    resB = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)

    #declare ctypes arguments
    imgR = np.asarray(self.img[:,:,0], order = 'C', dtype = ctypes.c_uint8)
    imgG = np.asarray(self.img[:,:,1], order = 'C', dtype = ctypes.c_uint8)
    imgB = np.asarray(self.img[:,:,2], order = 'C', dtype = ctypes.c_uint8)

    #call the super-resolution algorithm
    self.lib.alg(imgR, resR, self.yDim, self.xDim)
    self.res[frame,:,:,0] = resR

    self.lib.alg(imgG, resG, self.yDim, self.xDim)
    self.res[frame,:,:,1] = resG

    self.lib.alg(imgB, resB, self.yDim, self.xDim)
    self.res[frame,:,:,2] = resB

  def resolve(self, From = 0, length = None):

    #define range to resolve
    to = self.frames

    if length is not None:
      to = From + length

    #iterate over selected range to populate the result array
    for frame in range(From, to):

      self.exe(frame)
    
  
  def get_res(self):

    if self.frames == 1:
      return self.res[0]
    else:
      return self.res

    












                  

              




      