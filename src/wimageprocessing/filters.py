
__all__ = ['central_diff','sobel_diff','prewitt_diff','roberts_diff']

import numpy
import scipy.signal

"""
Toolbox of methods used for differanting an image
"""
def convolve(img,kernel,boundary='symm'):
    """
    The method used to convolve
    """
    return scipy.signal.convolve2d(img,kernel,'same',boundary)

def convolve_decompsited(img,kernel):
    """
    TODO use specialfunction scipy.signal sepfir2d, since we have separated filter (remember to reverse the direction to make a filter instead) and mirror symmetric boundary cond.
    AND use this for 
    """
    pass

#TODO write about pros/cons in these filters

def central_diff(img):
    kernel_central_x=numpy.matrix("1 0 -1",dtype=numpy.float64)
    kernel_central_y=numpy.matrix("1;0;-1",dtype=numpy.float64)
    return map(lambda kernel:convolve(img,kernel),[kernel_central_x,kernel_central_y])

def sobel_diff(img):
    kernel_sobel_x=numpy.matrix("-1 0 -1;-2 0 2;-1 0 1",dtype=numpy.float64)
    kernel_sobel_y=numpy.matrix("-1 -2 -1;0 0 0;1 2 1",dtype=numpy.float64)
    return map(lambda kernel:convolve(img,kernel),[kernel_sobel_x,kernel_sobel_y])

def prewitt_diff(img):
    kernel_prewitt_x=numpy.matrix("-1 0 1;-1 0 1;-1 0 1",dtype=numpy.float64)
    kernel_prewitt_y=numpy.matrix("-1 -1 -1;0 0 0;1 1 1",dtype=numpy.float64)
    return map(lambda kernel:convolve(img,kernel),[kernel_prewitt_x,kernel_prewitt_y])

def roberts_diff(img):
    kernel_roberts_x=numpy.matrix("1 0;0 -1",dtype=numpy.float64)
    kernel_roberts_y=numpy.matrix("0 1;-1 0",dtype=numpy.float64)
    return map(lambda kernel:convolve(img,kernel),[kernel_roberts_x,kernel_roberts_y])

def magic_diff(img):
    #Implement: http://assassinationscience.com/johncostella/edgedetect/
    pass


