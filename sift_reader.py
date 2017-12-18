#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import struct

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
        loc = struct.unpack('ff4cff', data[iStart:iStop])

        locations.append(loc)

    iDescStart = iStop

    descriptors = []
    for i in range(npoints):
        iStart = iDescStart + i * 128
        iStop = iStart + 128
        descriptors.append(data[iStart:iStop])

    return locations, descriptors


if __name__ == '__main__':
    fname = sys.argv[1]
    locations, descriptors = read_sift_file(fname)


