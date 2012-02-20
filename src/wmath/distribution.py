import numpy
from random import random

class distribution:
    """
    Distribution representation

    """

    __p=None
    __cumsum=None

    def __init__(self,p):
        """
        Constructor for distribution

        @Param p numpy-array representing the probability function, should be normalized
        """
        assert('cumsum' in dir(p))
        assert('searchsorted' in dir(p))
        self.__p=p

    def sample(self,n=1,sample_set=None):
        """
        Get n samples from the distribution

        @Param n the number of samples
        @Return vector of samples
        """
        if self.__cumsum is None:
            self.__cumsum=self.__p.cumsum()
        indices = [self.__cumsum.searchsorted(random()) for i in xrange(n)]
        if sample_set is None:
            return indices
        else:
            return map(lambda i:sample_set[i],indices)


if __name__== "__main__":
    import pylab
     
    for p in [numpy.array([0., 0., 1., 3., 5., 2., 0., 0., 5., 10., 5., 10., 12., 10., 2., 0., 0., 1., 2., 1.]),numpy.array([0.,0.,10.0,0.,0.,10.0,0.])]:

        psum=sum(p)
        p=numpy.array(map(lambda x:x/psum,p))
        
        d=distribution(p)
        N=100000
        sample=d.sample(N)

        i=numpy.arange(0,len(p),1)
        hist=map(lambda t:float(sample.count(t))/N,i)

        pylab.plot(i,p,i,hist,'*')

        pylab.show()
        raw_input("push 4 next")


