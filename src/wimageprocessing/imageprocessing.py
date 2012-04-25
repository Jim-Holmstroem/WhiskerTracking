
__all__= ['normalize','abs_edge','transform','histeq','histeqlocal','histogram','blur_gauss','dog']

import numpy

from ipmath import image_iterators
from scipy.ndimage import filters

"""
wip.function(img.array,argz...) #returns a copy with the result

Try to return everything that is calculated that might be used later

"""

"""
A little matlab code on realdata

img= imread('/misc/projects/whisker/video/video5-frames/frame-0250.png');
im = img(1:256,100+(1:256));
overlaycurves(im,njetedge(im,1,3,'valid'));

"""

def abs_edge(img,edge_filter=filters.prewitt):
    return numpy.sqrt(sum(map(lambda i:edge_filter(img,axis=i)**2,[0,1])))
    
def normalize(img):
    """
    normalizes the image
    """
    min,max=numpy.min(img),numpy.max(img) #returns extrems
    return (255.0/(max-min))*(img-min)

def transform(img,function):
    """
    Transform image pixels according to the function
    """
    raise NotImplementedError()

def histeq(img,histogram=None):
    """
    Lineary transform input range onto [0,1], to maximize contrast
    """
    raise NotImplementedError()

def histeqlocal(img,locality=5):
    raise NotImplementedError()

def histogram(img,bins,range=None):
    """
    Basically just a wrapper for:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html  
    """
    return numpy.histogram(img,bins,range)

def edge_response(img,detector):
    """
    """
    
    raise NotImplementedError()

def blur_gauss(img,delta,delta_clip=5):
    """
     
    Argument delta_clip where to clip the gauss kernel
    """
    
    raise NotImplementedError()

def dog(img,deltas):
    """
    DoG difference of gauss, to determine scale of things

    @Returns difference of gauss as a list of images
    """

    gauss_imgs = map(lambda delta:blur_gauss(img,delta), deltas)

    return map(lambda f:numpy.subtract([1],f[0]),image_iterator.pair_neighbours_inner(gauss_imags))
    



