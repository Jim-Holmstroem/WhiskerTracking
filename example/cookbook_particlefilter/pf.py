from numpy import *
from numpy.random import *


def resample(weights):
    n = len(weights)
    indices = []
    P = [0.] + [sum(weights[:i+1]) for i in range(n)] # accumulerade summan equlient to discrete integration (really bad complexity, bootstrap please)
    u0, j = random(), 0
    for u in [(u0+i)/n for i in range(n)]:
        while u > P[j]: #find index of first P[j] greater then u
            j+=1
        indices.append(j-1)
    return indices


def particlefilter(sequence, pos, stepsize, n):
    seq = iter(sequence)
    x = ones((n, 2), int) * pos                   # Initial position
    f0 = seq.next()[tuple(pos)] * ones(n)         # Target color model (start pixel from x0)'s color 
    yield pos, x, ones(n)/n                       # Return expected position, particles and weights

    for im in seq:
        x += normal(0, stepsize/4, x.shape)  # Particle motion model: uniform step
        x  = x.clip(zeros(2), array(im.shape)-1).astype(int) # Clip out-of-bounds particles, else something will try to access pixels outside the image (simply)
        f  = im[tuple(x.T)]                         # Measure particle colours (measure the particle)
        #f is a list of particle measurements        
        w  = 1./(1. + (f0-f)**2)                    # Weight~ inverse quadratic colour distance <-- 
        w /= sum(w)                                 # Normalize w
        yield sum(x.T*w, axis=1), x, w              # Return expected position, particles and weights
        if 1./sum(w**2) < n/2.:                     # If particle cloud degenerate:
            print "resample"
            x  = x[resample(w),:]                     # Resample particles according to weights
        else:
            print "y u no resample?"

if __name__ == "__main__":
    from pylab import *
    from itertools import izip
    import time
    ion()
    movie_length = 60
    seq = [ im for im in zeros((movie_length,600,600), int)]      # Create an image sequence of 20 frames long
    x0 = array([120, 160])                              # Add a square with starting position x0 moving along trajectory xs
    xs = vstack((arange(movie_length)*10, arange(movie_length)*2)).T + x0
    for t, x in enumerate(xs):
        xslice = slice(x[0]-8, x[0]+8)
        yslice = slice(x[1]-8, x[1]+8)

        xinverted = slice(x[1]-8, x[1]+8)
        yinverted = slice(x[0]-8, x[0]+8)


        xstatic = slice(x0[0]+10-4,x0[0]+10+4)
        ystatic = slice(x0[1]+20-4,x0[1]+20+4)

        seq[t][xslice, yslice] = 128
        seq[t][xinverted, yinverted] = 128
        seq[t][xstatic, ystatic] = 255




    for im, p in izip(seq, particlefilter(seq, x0, 64, 4*256)): # Track the square through the sequence
        pos, xs, ws = p
        position_overlay = zeros_like(im)
        position_overlay[tuple(pos)] = 1
        particle_overlay = zeros_like(im)
        particle_overlay[tuple(xs.T)] = 1
        hold(True)
        draw()
     #   time.sleep(0.3)
        clf()                                           # Causes flickering, but without the spy plots aren't overwritten
        imshow(im,cmap=cm.gray)                         # Plot the image
        spy(position_overlay, marker='.', color='b')    # Plot the expected position
        spy(particle_overlay, marker=',', color='r')    # Plot the particles
    show()


