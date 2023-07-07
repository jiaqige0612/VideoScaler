import numpy as np
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt

from PIL import Image

#open-source library for wavelet transform https://github.com/PyWavelets/pywt
import pywt
import pywt.data

import dtcwt
import dtcwt.compat
import dtcwt.sampling
#modified using code from https://github.com/rjw57/dtcwt
import dtcwt
import dtcwt.compat
import dtcwt.sampling

# Use an off-screen backend for matplotlib
# import matplotlib
# matplotlib.use('agg')

# Import numpy and matplotlib's pyplot interface
import numpy as np
#from matplotlib.pyplot import *

# Get a copy of the famous 'mandrill' image. In the default dtcwt tree, we ship
# one with the tests. The mandrill image is 512x512, floating point and has pixel
# values on the interval (0, 1].

def scale_waveletlanczos(ds_frame, scale = 2):

    def upscale(im):
        #scale low frequency sub-band
        return dtcwt.sampling.rescale(im, (im.shape[0]*scale, im.shape[1]*scale), 'lanczos')

    def upscale_hf(im):
        #scale high frequency sub-band
        return dtcwt.sampling.rescale_highpass(im, (im.shape[0]*scale, im.shape[1]*scale), 'lanczos')

    trans_result = np.empty((ds_frame.shape[0]*scale, ds_frame.shape[1]*scale, ds_frame.shape[2]))


    for i in range (3):

      # Transform ds_frame
      dsframe_l, dsframe_h = dtcwt.compat.dtwavexfm2(ds_frame[:, :, i], nlevels=1, biort='antonini')


      dsframe_l = upscale(ds_frame[:, :, i])

      dsframe_h_a = []

      for h in dsframe_h:
          print(h.shape)
          dsframe_h_a.append(upscale_hf(h))

      # Inverse transform
      trans_result[:, :, i] = dtcwt.compat.dtwaveifm2(dsframe_l, dsframe_h_a, biort='antonini')

    return trans_result
