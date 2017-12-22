#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import numpy as np
import matplotlib.pyplot as plt


goodDesc = np.array([
    11, 1, 1, 0, 0, 0, 0, 4, 73, 0, 0, 0, 0, 0, 0, 141, 127, 6, 10, 47,
    16, 1, 3, 141, 16, 4, 15, 141, 59, 11, 3, 9, 37, 2, 0, 0, 0, 0, 0, 4,
    141, 23, 8, 11, 0, 0, 0, 120, 69, 11, 15, 141, 62, 0, 1, 78, 0, 0, 1, 141,
    62, 0, 0, 0, 24, 12, 1, 0, 0, 0, 0, 0, 130, 135, 75, 27, 0, 0, 0, 3,
    12, 26, 89, 141, 13, 0, 0, 1, 0, 0, 5, 70, 9, 0, 0, 0, 1, 4, 2, 0,
    0, 0, 0, 0, 1, 23, 25, 3, 0, 0, 0, 0, 0, 3, 28, 19, 0, 0, 0, 0,
    1, 1, 4, 3, 0, 0, 0, 0])


lastGoodDesc = np.array([
    12, 3, 1, 0, 0, 5, 38, 26, 24, 0, 0, 0, 0, 5, 122, 58, 87, 1, 0, 0,
    0, 1, 42, 81, 28, 6, 4, 0, 0, 0, 0, 13, 65, 64, 14, 6, 2, 0, 3, 16,
    135, 74, 0, 0, 1, 7, 129, 76, 40, 4, 4, 8, 19, 29, 135, 71, 21, 36, 42, 13,
    14, 10, 13, 14, 78, 35, 26, 7, 2, 0, 0, 34, 135, 52, 1, 1, 5, 6, 6, 135,
    42, 1, 1, 19, 47, 48, 53, 36, 1, 3, 6, 64, 61, 30, 59, 18, 28, 2, 2, 0,
    0, 0, 0, 45, 77, 1, 6, 5, 2, 2, 4, 135, 7, 0, 10, 128, 37, 18, 23, 26,
    0, 0, 29, 135, 32, 2, 6, 3])


import sift

sift.init()
sift.RunSIFT_on_file('../data/test_eLab_building_01.jpg')

keys, descriptors = sift.GetFeatureVector()

numKeys = keys.shape[0]
numDescs = descriptors.shape[0]

assert numKeys == numDescs
numFeatures = int(numKeys)



from PIL import Image
im = Image.open('../data/test_eLab_building_01.jpg')

imBW = im.convert("L", matrix=(0.299, 0.587, 0.114, 0.0))

sift.RunSIFT(imBW.width, imBW.height, imBW.tobytes())


keys2, descriptors2 = sift.GetFeatureVector()


assert np.all(goodDesc == descriptors[0])
assert np.all(goodDesc == descriptors2[0])
assert np.all(lastGoodDesc == descriptors[-1])
assert np.all(lastGoodDesc == descriptors2[-1])

# Rounding errors, afaict:
assert (keys - keys2).max() < 0.001
assert (keys - keys2).min() > -0.001
# Keys are:  x, y, scale, orientation
# x and y are in pixels, so an error of ~0.001 pixels is perfectly fine
# min scale is 3.2, mean scale is 10, max scale is 453, so an error of ~0.001 seems fine

# Orientation errors are even smaller:
assert (keys[:, 3] - keys2[:, 3]).max() < 0.000003
assert (keys[:, 3] - keys2[:, 3]).min() > -0.000002

assert np.all(descriptors == descriptors2)

