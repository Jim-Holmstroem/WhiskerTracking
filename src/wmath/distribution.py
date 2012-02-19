import numpy
from random import random

class distribution:
    """
    Distribution representation

    """

    __cumsum=None

    def __init__(self,p):
        """
        Constructor for distribution

        @Param p numpy-array representing the probability function
        """
        __cumsum=p.cumsum()

    def sample(self,n=1):
        """

        @Param n the number of samples
        """
        return [self.__cumsum.searchsorted(random()) for i in range(n)]
