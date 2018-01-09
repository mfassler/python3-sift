#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import os
import struct
from PIL import Image
import numpy as np
import sift

import glob

def decode_yuyv(Y,U,V,w,h):
    # AJ equations
    R = Y + 1.403 * V
    G = Y - 0.344 * U - 0.714 * V
    B = Y + 1.770 * U

    R = R.reshape((h,w))
    G = G.reshape((h,w))
    B = B.reshape((h,w))
    R[R<0] = 0; R[R>255] = 255
    G[G<0] = 0; G[G>255] = 255
    B[B<0] = 0; B[B>255] = 255

    ar = np.array([R,G,B]).transpose(1,2,0)
    im = Image.fromarray(ar.astype(np.uint8), mode="RGB")
    return im;


files = glob.glob(os.path.expanduser('~/3dRecon/eLab2/*.yuyv_2448x2048'))
sift.init()

width = 2448
height = 2048


for oneFileName in files:
    data = open(oneFileName, 'rb').read()
    YUYV = np.fromstring(data, dtype=np.uint8)
    Y = YUYV[0::2]
    U = (YUYV[1::4].repeat(2)).astype(np.int16) - 128
    V = (YUYV[3::4].repeat(2)).astype(np.int16) - 128

    jpgOutputFileName = oneFileName.replace('yuyv_2448x2048', 'jpg')
    im = decode_yuyv(Y, U, V, width, height)
    im.save(jpgOutputFileName)

    print(oneFileName)
    sift.RunSIFT(width, height, Y.tobytes())

    keys, descriptors = sift.GetFeatureVector()

    # Sort by scale (2nd colunn of the "keys" array)
    rowsSortedByScale = keys[:,2].argsort()[::-1]  # descending

    sortedKeys = keys[rowsSortedByScale]
    sortedDescriptors = descriptors[rowsSortedByScale]

    siftOutputFileName = oneFileName.replace('yuyv_2448x2048', 'sift')

    outFile = open(siftOutputFileName, 'wb')

    outFile.write(b'SIFTV4.0')
    outFile.write(struct.pack('III', sortedKeys.shape[0], 5, 128))

    for oneRow in sortedKeys:
        x = oneRow[0]
        y = oneRow[1]
        #  I get rounding/interpolation errors on the color here compared to VisualSFM:
        try:
            r,g,b = im.getpixel((int(round(x)), int(round(y))))
        except:
            # the center of the feature might be off-image, so we have no color
            r,g,b = 0,0,0
        a = 0  # I assume this is alpha?
        scale = oneRow[2]
        orientation = -oneRow[3]  # No clue why VisualSFM puts a minus sign here...

        outFile.write(struct.pack('ffBBBBff', x, y, r, g, b, a, scale, orientation))

    for oneRow in sortedDescriptors:
        outFile.write(oneRow.tobytes())

    outFile.write(b'\xffEOF')
    outFile.close()





