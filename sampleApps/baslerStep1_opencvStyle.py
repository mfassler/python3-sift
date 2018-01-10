#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import os
import glob
import struct
import numpy as np
import matplotlib.pyplot as plt
import cv2


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

    # OpenCV uses BGR ordering:
    image = np.array([B,G,R], np.uint8).transpose(1,2,0)
    return image


def write_binary_sift_file(filename, colorImage, keys, descriptors):
    assert len(keys) == len(descriptors), "Number of keys and number of descriptors doesn't match"

    # Sort by scale (2nd colunn of the "keys" array)
    #rowsSortedByScale = keys[:,2].argsort()[::-1]  # descending

    #sortedKeys = keys[rowsSortedByScale]
    #sortedDescriptors = descriptors[rowsSortedByScale]

    outFile = open(filename, 'wb')

    outFile.write(b'SIFTV4.0')
    outFile.write(struct.pack('III', len(keys), 5, 128))

    for i in range(len(keys)):
        x, y = keys[i].pt
        try:
            r,g,b = colorImage[int(round(y)), int(round(x))]
        except:
            print("Warning, coord %d %d not found in colorImage" % (x, y))
            # the center of the feature might be off-image, so we have no color
            r,g,b = 0,0,0
        a = 0  # I assume this is alpha?
        scale = keys[i].size
        # OpenCV uses degrees, SiftGPU uses radians:
        # (... openCV also puts a minus sign here, hrmm.... )
        orientation = keys[i].angle * np.pi / 180.0

        outFile.write(struct.pack('ffBBBBff', x, y, r, g, b, a, scale, orientation))

    #for oneRow in sortedDescriptors:
    for oneRow in descriptors:
        outFile.write(oneRow.astype(np.uint8).tobytes())

    outFile.write(b'\xffEOF')
    outFile.close()


def loadImage(filename, width=2448, height=2048):
    data = open(filename, 'rb').read()
    YUYV = np.fromstring(data, dtype=np.uint8)
    Y = YUYV[0::2]
    U = (YUYV[1::4].repeat(2)).astype(np.int16) - 128
    V = (YUYV[3::4].repeat(2)).astype(np.int16) - 128
    colorImage = decode_yuyv(Y, U, V, width, height)
    # With YUYV, we get the bwImage for (nearly) free...
    bwImage = Y.reshape((height, width))
    return colorImage, bwImage


def showMe(_theImage):
    cv2.imshow('Ooh lala', _theImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


sift = cv2.xfeatures2d.SIFT_create()

files = glob.glob(os.path.expanduser('~/3dRecon/eLab2/*.yuyv_2448x2048'))

for oneFileName in files:
    print(oneFileName)
    colorImage, bwImage = loadImage(oneFileName)

    # jpgOutputFileName = oneFileName.replace('yuyv_2448x2048', 'jpg')
    # cv2.imwrite(jpgOutputFileName, colorImage)

    keypoints, descriptors = sift.detectAndCompute(bwImage, None)

    siftOutputFileName = oneFileName.replace('yuyv_2448x2048', 'sift')
    write_binary_sift_file(siftOutputFileName, colorImage, keypoints, descriptors)

