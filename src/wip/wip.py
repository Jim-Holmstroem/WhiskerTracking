import numpy
import scipy.signal

"""
A little matlab code on realdata

img= imread('/misc/projects/whisker/video/video5-frames/frame-0250.png');
im = img(1:256,100+(1:256));
overlaycurves(im,njetedge(im,1,3,'valid'));

"""

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

class wip:
    """
    wip.function(img.array,argz...) #returns a copy with the result
    
    Try to return everything that is calculated that might be used later

    """

    class wip_math:
        def norm(X,Y,p=2):
            """
            Elementwise norm

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

    class differential:

        def convolve(img,kernel):
            """
            The method used to convolve
            
            TODO use specialfunction scipy.signal sepfir2d, since we have separated filter (remember to reverse the direction to make a filter instead) and mirror symmetric boundary cond.
            """
            return scipy.signal.convolve2d(img,kernel,boundary='symm')

        def diff_x(img):
            kernel_diff_x=numpy.matrix("1 0 -1",dtype=numpy.float64)
            scipy.signal.convolve2d( 
        
        def diff_y(img):
            kernel_diff_y=numpy.matrix("1;0;-1",dtype=numpy.float64)
            make a map instead?

        class gradient:
            """
            Lazy gradient class that takes a reference to an image and calculates necassary parameters as they are called.
            
            Updating the image will invalidate all data, you can call renew (you might as well make a new instance)


            """
            # == HANDLING ==
            self.diff_x=None #the differentation function 
            self.diff_y=None
            
            # == DATA ==
            self.dx=None #the image differantiated in one direction
            self.dy=None
            self.mag=None
            self.dir=None
            
            def __init__(self,img,diff_x=differential.diff_x,diff_y=differential.diff_y):
                self.img=img
                self.diff_x=diff_x
                self.diff_y=diff_y
          
            def renew(self,img):
                self.img=img
                self.dx=None 
                self.dy=None
                self.mag=None
                self.dir=None

            def dx(self):
                if self.dx is None:
                    self.dx=self.diff_x(self.img)    
                return self.dx

            def dy(self):
                if self.dy is None:
                    self.dy=self.diff_y(self.img)    
                return self.dy

            def mag(self):
                if self.mag is None:
                    self.mag = wip_math.norm(self.dx,self.dy,2)
                return self.mag

            def dir(self):
                if self.dir is None:
                    self.dir=wip_math.direction(grad.x,grad.y)
                return self.dir

        def diff(self,img):
            return gradient(img)

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
        Wrapper for:
        http://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html  
        """
        pass

    def edge_response(img,detector):
        """
        """
        pass

    def gauss(img,delta):
        """
        """
        raise NotImplementedError()

    def dog(img,deltas):
        """
        DoG difference of gauss, to determine scale of things

        @Returns difference of gauss as a list of images
        """
        raise NotImplementedError()
        
    def find_features(img,detector,threshold):
        """
        
        @Returns a list of feature responses above treshold
        """
        #localmax? how to search for them?
        #return filter(lambda feature: feature.fitness>threshold,features)

        raise NotImplementedError()

