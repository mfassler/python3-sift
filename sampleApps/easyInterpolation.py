
import math


# Based on https://en.wikipedia.org/wiki/Bilinear_interpolation
#   section titled "Unit square"


def interpolate(x, y, img):

    x_0 = math.floor(x)
    x_1 = math.ceil(x)
    y_0 = math.floor(y)
    y_1 = math.ceil(y)

    x_frac = x - x_0
    x_inv = 1 - x_frac
    y_frac = y - y_0
    y_inv = 1 - y_frac

    # x and y are reversed in img?

    a = img[y_0, x_0] * x_inv  * y_inv
    b = img[y_0, x_1] * x_frac * y_inv
    c = img[y_1, x_0] * x_inv  * y_frac
    d = img[y_1, x_1] * x_frac * y_frac

    return a+b+c+d

