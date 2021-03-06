from itertools import repeat
from parallel import parallel_map
from random import uniform
from wmath import weighted_choice, distribution
import numpy

def default_sampler(X_prev):
    raise NotImplementedError()

'''
Randomly chooses samples from X with replacement, weighted according to weights.
'''
def default_resample(X, weights):
    raise Exception("Shouldn't be used")
    return numpy.array(map(weighted_choice, weights, X))

'''
Better version of default_resample, uses wmath.distribution instead which is
O(log n) for getting a sample in a population of size n
'''
def better_resample(X, weights):
    return numpy.array(distribution(weights).sample(X.shape[0], X))

def low_variance_resample(X, weights):
    X_bar = numpy.zeros_like(X)

    M = len(X)
    M_inv = 1.0/M
    r = uniform(0,M_inv) # Random number between 0 and M_inv
    c = weights[0]

    j = 0
    i = 0
    
    for m in xrange(M):
        u = r + m * M_inv
        while u > c:
            i += 1
            c += weights[i]
        
        X_bar[j] = X[i]
        j += 1
    
    return X_bar

'''
pf
@param X_prev
'''
def pf(X_prev, observation, importance_function, sampling_function=default_sampler, resampling_function=better_resample):

    X_bar = numpy.array(map(sampling_function, X_prev)) # TODO: vectorize this
    weights = numpy.array(map(importance_function, zip(X_bar, repeat(observation, len(X_bar)))))
    
    if weights.sum() == 0:
        weights = numpy.ones_like(weights) / float(weights.size)
    else:
        weights /= float(weights.sum())
    
    return resampling_function(X_bar, weights), X_bar
