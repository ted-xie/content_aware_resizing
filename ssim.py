"""
===========================
Structural similarity index
===========================

When comparing images, the mean squared error (MSE)--while simple to
implement--is not highly indicative of perceived similarity.  Structural
similarity aims to address this shortcoming by taking texture into account
[1]_, [2]_.

.. [1] Zhou Wang; Bovik, A.C.; ,"Mean squared error: Love it or leave it? A new
       look at Signal Fidelity Measures," Signal Processing Magazine, IEEE,
       vol. 26, no. 1, pp. 98-117, Jan. 2009.

.. [2] Z. Wang, A. C. Bovik, H. R. Sheikh and E. P. Simoncelli, "Image quality
       assessment: From error visibility to structural similarity," IEEE
       Transactions on Image Processing, vol. 13, no. 4, pp. 600-612,
       Apr. 2004.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

from skimage.measure import compare_ssim as ssim
from skimage.transform import resize as skresize
from skimage import color, io

if len(sys.argv) != 3:
    print("Usage: python ssim.py <image1> <image2>")
    exit()

file1 = sys.argv[1]
file2 = sys.argv[2]

img1 = color.rgb2gray(io.imread(file1, mode="RGB"))
img2 = color.rgb2gray(io.imread(file2, mode="RGB"))

# need to make sure image dimensions match
orig_shape = img1.shape
img2 = skresize(img2, img1.shape, mode="reflect")

def mse(x, y):
    return np.linalg.norm(x - y)

mse_val = mse(img1, img2)
ssim_val = ssim(img1, img2, data_range=(img2.max() - img2.min()))

print("MSE: %f, SSIM: %f" % (mse_val, ssim_val))

