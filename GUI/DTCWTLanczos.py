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
import matplotlib
matplotlib.use('agg')

# Import numpy and matplotlib's pyplot interface
import numpy as np
from matplotlib.pyplot import *

# Get a copy of the famous 'mandrill' image. In the default dtcwt tree, we ship
# one with the tests. The mandrill image is 512x512, floating point and has pixel
# values on the interval (0, 1].

def scale_waveletlanczos(ds_frame):

    mandrill = ds_frame


    # We will try to re-scale mandrill by this amount and method
    scale = 2
    scale_method = 'lanczos'

    def scale_direct(im):
        """Scale image directly."""
        return dtcwt.sampling.rescale(im, (im.shape[0]*scale, im.shape[1]*scale), scale_method)
        #return dtcwt.sampling.upsample(im,scale_method)

    def scale_highpass(im):
        """Scale image assuming it to be wavelet highpass coefficients."""
        return dtcwt.sampling.rescale_highpass(im, (im.shape[0]*scale, im.shape[1]*scale), scale_method)
        #return dtcwt.sampling.upsample_highpass(im, scale_method)

    trans_result = np.empty((ds_frame.shape[0]*scale, ds_frame.shape[1]*scale, ds_frame.shape[2]))


    for i in range (3):
      # Rescale mandrill directly using default (Lanczos) sampling
      #mandrill_direct = scale_direct(mandrill[:,:,i])

      # Transform mandrill
      #one level
      mandrill_l, mandrill_h = dtcwt.compat.dtwavexfm2(mandrill[:, :, i], nlevels=1, biort='antonini', qshift= 'qshift_b_bp')


      mandrill_l = scale_direct(mandrill[:, :, i])

      mandrill_h_b = []

      for h in mandrill_h:
          print(h.shape)
          mandrill_h_b.append(scale_highpass(h))

      # Transform back
      mandrill_b = dtcwt.compat.dtwaveifm2(mandrill_l, mandrill_h_b, biort='antonini', qshift= 'qshift_b_bp')

      trans_result[:, :, i] = mandrill_b

    return trans_result
