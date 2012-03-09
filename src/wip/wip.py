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

    """
    def transform(img,function):
        """
        Transform image pixels according to the function
        """
        raise NotImplementedError()

    def histeq(img):
        """
        Lineary transform input range onto [0,1]
        """
        raise NotImplementedError()

    def histeqlocal(img,locality=5):
        raise NotImplementedError()

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

