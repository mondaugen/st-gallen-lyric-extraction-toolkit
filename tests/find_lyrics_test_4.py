# Trying out the convolution kernels to do 'blurry' horizontal projections
# This could perhaps be used as a replacement to merely using one row of the
# image for each horizontal projection value.
#
# arguments are:
#
# path to image
# path to desination directory

from gamera.core import *
from gamera.plugins import convolution
import sys
import time
import os

init_gamera()

# Ensure that image is rgb
img = load_image(sys.argv[1]).to_rgb()

kern = convolution.GaussianKernel(100.0)

convolved = img.convolve_y(kern)

# Prepare a path where the resulting image will be saved to
pathprepend = sys.argv[2]

imagedir = pathprepend + "/convolved_y_" + time.strftime("%y-%m-%d")

try:
  os.mkdir(imagedir)
except OSError as e:
  print "Directory already exists, but that's cool."

imagepath = imagedir + "/" + time.strftime("%H_%M_%S")\
    +"-"+os.path.basename(sys.argv[1])

# Save the image
onebit = convolved.to_onebit()
onebit.save_PNG(imagepath)
