#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import numpy as np
import matplotlib.pyplot as plt


goodDesc = np.array([
    29, 1, 0, 5, 159, 2, 0, 0, 169, 5, 0, 0, 12, 1, 0, 8, 72, 1, 0, 0,
    22, 7, 0, 4, 0, 0, 0, 1, 15, 4, 0, 0, 36, 0, 0, 1, 169, 14, 0, 0,
    169, 4, 0, 0, 18, 1, 0, 3, 98, 1, 0, 2, 29, 4, 0, 1, 0, 0, 0, 1,
    17, 10, 0, 0, 32, 0, 0, 0, 169, 18, 0, 2, 169, 2, 0, 0, 19, 2, 0, 9,
    97, 1, 0, 3, 13, 12, 2, 3, 0, 0, 0, 1, 13, 15, 1, 0, 27, 1, 0, 6,
    165, 3, 0, 1, 169, 3, 0, 1, 15, 1, 0, 6, 73, 1, 1, 6, 8, 5, 0, 3,
    0, 0, 0, 2, 11, 7, 0, 0])


lastGoodDesc = np.array([
    3, 3, 4, 4, 0, 0, 1, 1, 14, 44, 77, 41, 1, 1, 1, 2, 10, 35, 141, 23,
    5, 13, 10, 9, 0, 1, 52, 41, 8, 16, 4, 0, 4, 14, 43, 15, 1, 1, 1, 1,
    61, 48, 136, 146, 21, 1, 1, 5, 146, 92, 75, 36, 26, 114, 66, 84, 15, 9, 39, 56,
    108, 146, 34, 11, 5, 4, 3, 4, 2, 1, 0, 2, 82, 12, 8, 52, 34, 0, 0, 38,
    146, 62, 41, 73, 15, 10, 2, 75, 13, 14, 42, 121, 67, 68, 2, 5, 0, 0, 0, 0,
    0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 10, 0, 1, 12, 1, 0, 0, 6,
    1, 0, 2, 12, 1, 0, 0, 2])


import sift

sift.init()
sift.RunSIFT_on_file('/home/fassler/3dRecon/bikeModel/DJI_0085.JPG')

keys, descriptors = sift.GetFeatureVector()

numKeys = len(keys) / 4.0
numDescs = len(descriptors) / 128.0

assert numKeys == numDescs
numFeatures = int(numKeys)

keys = np.array(keys).reshape(numFeatures, 4)
descriptors = np.array(descriptors, np.uint8).reshape(numFeatures, 128)

'''
loc = np.array(stuff[0:4])
desc = np.array(stuff[4:132])

lastLoc = np.array(stuff[-132:-128])
lastDesc = np.array(stuff[-128:])
'''


from PIL import Image
im = Image.open('/home/fassler/3dRecon/bikeModel/DJI_0085.JPG')

imBW = im.convert("L")
sift.RunSIFT(imBW.width, imBW.height, imBW.tobytes())

'''
raw = im.tobytes()
numPixels = int(len(raw)/3)
bw = b''

bwArray = np.empty((numPixels), np.uint8)

for i in range(numPixels):
    r = raw[i*3]
    g = raw[i*3+1]
    b = raw[i*3+2]
    onePixel = 0.28965*r + 0.60581*g + 0.10454*b
    bwArray[i] = int(onePixel)
'''


