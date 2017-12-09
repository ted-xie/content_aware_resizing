import argparse
# scipy imports
from scipy import ndimage
from scipy import misc
# numpy imports
import numpy as np
# matplotlib imports
import matplotlib.pyplot as plt
# skimage imports
from skimage import color
from skimage import io
# local imports
from img_ops import resize

# Argument parser
parser = argparse.ArgumentParser(description="Perform content-aware resizing")
parser.add_argument("-i", "--img", required=True, help="Input image name")
parser.add_argument("-o", "--output", required=False, help="(Optional) Output image name, default to out_<image_name")
parser.add_argument("-nx", "--xpixels", required=True, help="Number of pixels to reduce in the X-dimension")
parser.add_argument("-ny", "--ypixels", required=True, help="Number of pixels to reduce in the Y-dimension")
parser.add_argument("-s", "--show", required=False, help="show the output image compared to the original", action="store_true")
parser.add_argument("-a", "--algo", required=False, help="Which algorithm to use: greedy, random, dijkstra")

args = parser.parse_args()

img = color.rgb2gray(io.imread(args.img, mode="RGB"))

# Initially set outfile path to be "out_"+<image_name>
# If output path is specified, use that instead
output_file_path = "out_" + args.img
if args.output:
    output_file_path = args.output

algo = "greedy"
if args.algo:
    algo = args.algo

# Cast command line args to string
nx = int(args.xpixels)
ny = int(args.ypixels)

# First resize by X dimension
result = resize(img, nx, algo)

# Then resize by Y dimension
# This can be done by rotating by 90 degrees and repeating the resize algo
result = ndimage.rotate(result, 90)
result = resize(result, ny, algo)

# Rotate back to original orientation
result = ndimage.rotate(result, 270)

orig_shape = np.shape(img)
new_shape = np.shape(result)
print("Original dimensions: xdim=%d, ydim=%d" % (orig_shape[0], orig_shape[1]))
print("New dimensions: xdim=%d, ydim=%d" % (new_shape[0], new_shape[1]))

# Write out result
misc.imsave(output_file_path, result)

# Show the result if specified
if args.show:
    plt.subplot(2,1,1)
    plt.imshow(img, cmap="gray")
    plt.title("Original image")

    plt.subplot(2,1,2)
    plt.imshow(result, cmap="gray")
    plt.title("Resulting image")
    plt.show()

    plt.axis("off") # don't show X and Y axis
