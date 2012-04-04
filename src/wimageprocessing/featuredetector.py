
__all__=[]

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


def find_features(img,detector,threshold):
    """
    
    @Returns a list of feature responses above treshold
    """
    #localmax? how to search for them?
    #return filter(lambda feature: feature.fitness>threshold,features)

    raise NotImplementedError()


