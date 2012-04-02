
__all__=['wip','image_gradient','central_diff','sobel_diff','prewitt_diff','roberts_diff','filter_image','filter_video']

import itertools 

import numpy
import scipy.signal

from wmedia import wimage,wvideo

"""
A little matlab code on realdata

img= imread('/misc/projects/whisker/video/video5-frames/frame-0250.png');
im = img(1:256,100+(1:256));
overlaycurves(im,njetedge(im,1,3,'valid'));

"""

#================== [ FILTERS ] ========================

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


#=============== [ MATH ] ===================================

def norm(X,Y,p=2):
    """
    Elementwise norm |(x_ij,y_ij)|_p

    Preferably X.shape=Y.shape but numpy 
    handles others, see numpy broadcastable
    
    Note. The == operator with float("inf") is a little 
    bit contriversial but it works in this case.

    Returns c_ij=(x_ij^p+y_ij^p)^(1/p)
    """
    if(p==2): #Euclidian
        return numpy.sqrt(numpy.add(numpy.square(X),numpy.square(Y)))
    elif(p==1): #Manhattan
        return numpy.add(numpy.absolute(X),numpy.absolute(Y))
    elif(p==float("inf")): #Maximum norm (special case of: inf-norm)
        return numpy.maximum(numpy.absolute(X),numpy.absolute(Y))
    else:
        return numpy.power(numpy.add(numpy.power(X,p),numpy.power(Y,p)),1./p)

def direction(X,Y):
    """
    Elementwise direction

    Uses special function arctan2 used for this type of problems and
    should handle specialcase
    """
    return numpy.arctan2(Y,X)

class point:
    """
    point is a container that has a x and y value

    """
    def __init__(self,x=None,y=None,p=None):
        """
        Either takes x,y or a 2-vector p
        """
        if not p is None and (not x is None or not y is None):
            return ValueError("Cant spec (x,y) AND p")
        
        if p is None:
            self.x=x
            self.y=y
        else:
            self.x=p[0]
            self.y=p[1]

#================= [ UTILS ] ============================

"""
A filter is basically a function f: img->img (if there are parameters they would have to be lambdad out)
"""
def filter_image(img,f=None):
    return wimage(f(img))
def filter_video(video,f=None):
    return wvideo(map(f,video))

#================ [ FEATURE DETECTION ] =================

class feature:
    """
    Virtual baseclass for features

    """

    fitness=0 #How good is the feature

    def draw(self,context):
        """
        Debug draw the feature on image
        """
        pass

class feature_detector:
    pass

class edge_detector:
    """
    Virtual baseclass for edge detectors
    """
    def response(self,img):
        pass

#============ [ IMAGE PROCESSING ] ==========================

"""
wip.function(img.array,argz...) #returns a copy with the result

Try to return everything that is calculated that might be used later

"""

def gray(img):
    return numpy.divide(numpy.add.reduce(img,2),img.shape[2])

class wip_iter:
    def pair_neighbours_inner(v):
        """
       
        Note. the same idea can be made to handle different boundary conditions (copy, ignore, rotation) [izip([v[],v+[v[-1]])]
        
        Returns all the inner neighbouring elements as pairs (v_i,v_{i+1})

        """
        return zip(v[:-1],v[1:])

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

    return map(lambda f:numpy.subtract([1],f[0]),wip_iter.pair_neighbours_inner(gauss_imags))
    
def find_features(img,detector,threshold):
    """
    
    @Returns a list of feature responses above treshold
    """
    #localmax? how to search for them?
    #return filter(lambda feature: feature.fitness>threshold,features)

    raise NotImplementedError()



class image_gradient:
    """
    Lazy gradient class that takes a reference to an image and calculates necassary parameters as they are called.
    
    Updating the image will invalidate all data, you can call renew (you might as well make a new instance)

    """
    diffs_data=None
    mag_data=None
    dir_data=None
    
    def __init__(self,img,diff_method=central_diff):
        """

        Argument img the image to take the gradient of
        Argument diff_method takes image and returns [diff_x,diff_y]
        """
        self.img=img
        self.diff_method=diff_method
  
    def renew(self,img):
        self.img=img
        self.diffs_data=None
        self.mag_data=None
        self.dir_data=None

    def diffs(self):
        """
        Returns a point containing the diff in x and y 
        """
        if self.diffs_data is None:
            self.diffs_data = point(self.diff_method(self.img))
        return self.diffs_data

    def mag(self):
        if self.mag_data is None:
            self.mag_data = norm(self.diffs().x,self.diffs().y,self.diffs(),2)
        return self.mag_data

    def dir(self):
        if self.dir_data is None:
            self.dir_data=direction(self.diffs().x,self.diffs().y)
        return self.dir_data



