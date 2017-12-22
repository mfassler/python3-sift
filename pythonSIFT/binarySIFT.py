#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


###  This should produce binary SIFT files that are identical* to those 
###  produced by VisualSFM.
###
### (*there are some tiny rounding errors and interpolation errors...)
###

import sys
import struct
from PIL import Image
import numpy as np
import sift

sift.init()

if __name__ == '__main__':
    inFileName = sys.argv[1]
    outFileName = sys.argv[2]

    im = Image.open(inFileName)
    imBW = im.convert("L", matrix=(0.299, 0.587, 0.114, 0.0))

    sift.RunSIFT(imBW.width, imBW.height, imBW.tobytes())

    keys, descriptors = sift.GetFeatureVector()

    # Sort by scale (2nd colunn of the "keys" array)
    rowsSortedByScale = keys[:,2].argsort()[::-1]  # descending

    sortedKeys = keys[rowsSortedByScale]
    sortedDescriptors = descriptors[rowsSortedByScale]

    # The output file format is described in:
    #  http://ccwu.me/vsfm/doc.html
    # (should be readable by sift_reader.py)

    outFile = open(outFileName, 'wb')

    outFile.write(b'SIFTV4.0')
    outFile.write(struct.pack('III', sortedKeys.shape[0], 5, 128))

    for oneRow in sortedKeys:
        x = oneRow[0]
        y = oneRow[1]
        #  I get rounding/interpolation errors on the color here compared to VisualSFM:
        r,g,b = im.getpixel((int(round(x)), int(round(y))))
        a = 0  # I assume this is alpha?
        scale = oneRow[2]
        orientation = -oneRow[3]  # No clue why VisualSFM puts a minus sign here...

        outFile.write(struct.pack('ffBBBBff', x, y, r, g, b, a, scale, orientation))

    for oneRow in sortedDescriptors:
        outFile.write(oneRow.tobytes())

    outFile.write(b'\xffEOF')
    outFile.close()



