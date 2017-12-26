#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import struct
import numpy as np


def read_sift_file(filename):

    f = open(filename, 'rb')
    data = f.read()
    f.close()

    assert data[0:4] == b'SIFT'

    # expecting something like: "V4.0"
    char_v, major_version, char_dot, minor_version = struct.unpack('cccc', data[4:8])
    assert char_v == b'V'
    assert char_dot == b'.'

    major_version = int(major_version, 10)
    minor_version = int(minor_version, 10)

    assert major_version == 4 or major_version == 5
    assert minor_version == 0

    assert data[-4:] == b'\xffEOF'

    npoints, int5, int128 = struct.unpack('III', data[8:20])

    assert int5 == 5
    assert int128 == 128

    HEADER_SIZE = 20
    EOF_SIZE = 4

    location_size = npoints * 4 * 5
    descriptor_size = npoints * 128

    assert len(data) == (HEADER_SIZE + location_size + descriptor_size + EOF_SIZE)

    locations = []
    for i in range(npoints):
        iStart = HEADER_SIZE + i * 4 * 5
        iStop = iStart + 4 * 5
        loc = struct.unpack('ff4Bff', data[iStart:iStop])

        locations.append(loc)

    iDescStart = iStop
    iDescStop = iDescStart + descriptor_size

    descriptors = np.fromstring(data[iDescStart:iDescStop], dtype=np.uint8).reshape((npoints, 128))

    return locations, descriptors


if __name__ == '__main__':
    fname = sys.argv[1]
    locations, descriptors = read_sift_file(fname)
    # This should match the output from the library (except that sort order is random):
    keys = np.empty((len(locations), 4))
    for i in range(len(locations)):
        oneLoc = locations[i]
        x, y, s, o = oneLoc[0], oneLoc[1], oneLoc[6], oneLoc[7]
        keys[i] = np.array([x, y, s, o])

