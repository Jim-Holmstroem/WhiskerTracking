'''
Created on Feb 20, 2012

@author: Emil Lundberg
'''

import numpy
import pylab
from wmath import distribution

weights = numpy.arange(25)
weights = weights/float(weights.sum())

num_samples = 100000
d = distribution(weights)
sample = d.sample(num_samples)

frequencies = numpy.array([sample.count(i) for i in xrange(weights.size)])

pylab.plot(weights, weights/float(sum(weights)))
pylab.plot(weights, frequencies/float(sum(frequencies)), "b*")
pylab.show()
