import numpy
import matplotlib.pylab as plot
from wmath import weighted_choice

weights = numpy.arange(25)
num_samples = 100000
frequencies = numpy.zeros_like(weights)

for i in xrange(num_samples):
    frequencies[weighted_choice(weights)] += 1

plot.plot(weights, weights/float(sum(weights)))
plot.plot(weights, frequencies/float(num_samples), "b*")
plot.show()
