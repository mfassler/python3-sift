
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


from distutils.core import setup, Extension

module1 = Extension('sift',
                    libraries = ['siftgpu'],
                    library_dirs = ['/usr/local/lib'],
                    sources = ['siftmodule.cpp'])

setup (name = 'sift',
       version = '1.0',
       description = 'The SIFT feature detector and matcher, with GPU acceleration',
       ext_modules = [module1])
