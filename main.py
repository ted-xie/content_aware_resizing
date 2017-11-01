import argparse

from scipy import ndimage
from scipy import misc

import matplotlib.pyplot as plt

from img_ops import resize

# Argument parser
parser = argparse.ArgumentParser(description="Perform content-aware resizing")
parser.add_argument("-i", "--img", required=True, help="Input image name")
parser.add_argument("-o", "--output", required=False, help="(Optional) Output image name, default to out_<image_name")
parser.add_argument("-nx", "--xpixels", required=True, help="Number of pixels to reduce in the X-dimension")
parser.add_argument("-ny", "--ypixels", required=True, help="Number of pixels to reduce in the Y-dimension")

args = parser.parse_args()

img = misc.imread(args.img)

# Initially set outfile path to be "out_"+<image_name>
# If output path is specified, use that instead
output_file_path = "out_" + args.img
if (args.output):
    output_file_path = args.output

# First resize by X dimension
result = resize(img, args.xpixels)

# Then resize by Y dimension
# This can be done by rotating by 90 degrees and repeating the resize algo
result = ndimage.rotate(result, 90)
result = resize(result, args.ypixels)

# Rotate back to original orientation
result = ndimage.rotate(result, 270)

# Write out result
misc.imsave(output_file_path, result)
