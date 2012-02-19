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

        @Param p numpy-array representing the probability function
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
        indices = [self.__cumsum.searchsorted(random()) for i in range(n)]
        if sample_set is None:
            return indices
        else:
            return map(lambda i:sample_set[i],indices)
