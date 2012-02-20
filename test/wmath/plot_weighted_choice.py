'''
Created on Feb 20, 2012

@author: Emil Lundberg
'''

import numpy
import pylab
from wmath import weighted_choice

weights = numpy.arange(25)
num_samples = 100000
frequencies = numpy.zeros_like(weights)

for i in xrange(num_samples):
    frequencies[weighted_choice(weights)] += 1

pylab.plot(weights, weights/float(sum(weights)))
pylab.plot(weights, frequencies/float(num_samples), "b*")
pylab.show()
