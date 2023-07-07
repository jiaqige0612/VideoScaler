#This script implements all necessary tools to super-resolve images and video using the
#local structure estimation methods V1, V2 and V3 as detailed in the documentation.



import time
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import math 
import matplotlib.pyplot as plt
import cv2 
import subprocess 
import os

class ClocalStruct(object):

  def __init__(self, method, xDim, yDim, frames=1,  img=None):


    self.xDim = xDim
    self.yDim = yDim
    self.frames = frames

    self.img = img

    cwd = os.getcwd()
    cwd = cwd.replace("\\", "/")


    try:
      subprocess.run(["gcc", "--version"])
      compiler = "gcc"
    except:
      try:
        subprocess.run(["clang", "--version"])
        compiler = "clang"
      except:
        print("You do not have a supported compiler installed. Please install GCC or LLVM.")
    finally:
      print("detected {}, compiling dynamic libraries...".format(compiler))
      
    build_cmd = "{}/Algorithms/Clocalstruct/build_{}.sh".format(cwd, compiler)

    print(subprocess.call(["C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe", build_cmd]))

    #setup C libraries
    self.lib = ctypes.cdll.LoadLibrary('./algorithms/Clocalstruct/lib/{}.so'.format(method))

    self.alg = self.lib.alg

    self.alg.argtypes = [ndpointer(ctypes.c_uint8, flags="C_CONTIGUOUS"), ndpointer(ctypes.c_uint8, flags = "C_CONTIGUOUS"), ctypes.c_uint32, ctypes.c_uint32]

    #initialise result array
    
    self.res = np.empty(shape = (frames, yDim*2, self.xDim*2, 3), dtype = np.uint8)

    



  def exe(self, frame, frame_id):


    #declare ctypes result arrays
    resR = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)

    

    #declare ctypes arguments
    if(len(frame.shape) == 3):
      
      resG = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)
      resB = np.empty(shape = (self.yDim*2, self.xDim*2), dtype = ctypes.c_uint8)

      imgR = np.asarray(frame[:,:,0], order = 'C', dtype = ctypes.c_uint8)
      imgG = np.asarray(frame[:,:,1], order = 'C', dtype = ctypes.c_uint8)
      imgB = np.asarray(frame[:,:,2], order = 'C', dtype = ctypes.c_uint8)
      
      #call the super-resolution algorithm
      self.lib.alg(imgR, resR, self.yDim, self.xDim)
      self.res[frame_id,:,:,0] = resR

      self.lib.alg(imgG, resG, self.yDim, self.xDim)
      self.res[frame_id,:,:,1] = resG

      self.lib.alg(imgB, resB, self.yDim, self.xDim)
      self.res[frame_id,:,:,2] = resB
    
    else:

      img = np.asarray(frame, order = 'C', dtype = ctypes.c_uint8)

      print("hello", img.shape, resR.shape, self.yDim, self.xDim)

      self.lib.alg(img, resR, self.yDim, self.xDim)
      self.res[0,:,:,0] = resR
    




  def resolve(self, From = 0, length = None):

    #define range to resolve
    to = self.frames

    if length is not None:
      to = From + length
    
    if(self.frames == 1):
      self.exe(self.img, 0)
      return

    #iterate over selected range to populate the result array
    for i in range(From, to):

      self.exe(self.img[i], i)
    
  
  def get_res(self):

    if self.frames == 1:
      if(len(self.img.shape) == 3):
        return self.res[0].astype(np.uint8)
      else:
        return self.res[0,:,:,0]
    else:
      if(len(self.img[0].shape == 3)):
        return self.res.astype(np.uint8)
      else:
        return self.res[:,:,:,0]

    












                  

              




      