import numpy
import matplotlib.pyplot as plot
from math import exp, pi, sqrt
from wmath import distribution

class Tester:
    i=0

    def test(self, weights, num_samples=10000):
        plot.figure(self.i)
        self.i+=1
        
        weights = weights/float(weights.sum())
    
        d = distribution(weights)
        sample = d.sample(num_samples)
        
        frequencies = numpy.array([sample.count(i) for i in xrange(weights.size)])
        
        plot.plot(numpy.arange(weights.size), weights/float(sum(weights)))
        plot.plot(numpy.arange(weights.size), frequencies/float(sum(frequencies)), "b*")

t=Tester()

def test(weights):
    t.test(weights)

### Linear function ###
test(numpy.arange(50))

### Step function ###
test(numpy.array([0]*25+[1]*25))

### Step function the other way ###
test(numpy.array([1]*25+[0]*25))

### Alternator ###
test(numpy.array([0,1]*25))

### Gauss ###
test(numpy.array([1/(sqrt(2*pi)) * exp(-(x*x)/2) for x in numpy.linspace(-5, 5, 50)]))

### Plot the results ###
plot.show()
