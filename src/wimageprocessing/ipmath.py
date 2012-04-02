
__all__=['norm','direction','point','image_iterators']

import itertools 
import numpy

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

class image_iterators:
    def pair_neighbours_inner(v):
        """
       
        Note. the same idea can be made to handle different boundary conditions (copy, ignore, rotation) [izip([v[],v+[v[-1]])]
        
        Returns all the inner neighbouring elements as pairs (v_i,v_{i+1})

        """
        return zip(v[:-1],v[1:])


