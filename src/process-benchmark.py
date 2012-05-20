import matplotlib.pyplot as plt
import numpy
import os
import pylab
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter

absolute_error_path_pattern = "/misc/projects/whisker/results/GWhiskerTracker_n=%i_p=%i_a=%i_g=%i_s=%s/absolute_error.npy"

sigma_limits = numpy.array((0.000016, 0.004, 1))/10

err_norms = (2, 4, 8)
num_whiskers = 6
nn = (64, 128, 256, 512)
pp = (2, 4, 8)
aa = (1, 2, 4, 8)
gg = (1, 2, 4, 8)
ss = (0.25, 0.5, 1, 2, 4)

tensor_dim = (len(err_norms), len(nn), len(pp), len(aa), len(gg), len(ss), num_whiskers)

E = numpy.ones(tensor_dim) * 1E18

for ni, n in enumerate(nn):
    for pi, p in enumerate(pp):
        for ai, a in enumerate(aa):
            for gi, g in enumerate(gg):
                for si,s in enumerate(ss):
                    
                    path = absolute_error_path_pattern%(n,p,a,g,s*sigma_limits)
                    
                    if not os.path.exists(path):
#                        print "Did not find n=%i, p=%i, a=%i, g=%i, s=%i"%(n,p,a,g,s)
                        continue
                    
                    absolute_errors = numpy.load(path)
                    absolute_rms_time = ((absolute_errors**2).mean(axis=2))**0.5
#                    print absolute_rms_time
#                    print absolute_rms_time.max(axis=0)
                    for i, norm in enumerate(err_norms):
                        E[i,ni,pi,ai,gi,si,:] = absolute_rms_time[:,i]

def get_params_for_index(index):
    return (nn[index[0]], pp[index[1]], aa[index[2]], gg[index[3]], ss[index[4]])

for i, P in enumerate(err_norms):
    maxerr = E[i].max(axis=5)
    
    best_maxerr = numpy.where(maxerr == maxerr.min())
    best = numpy.where(E[i] == E[i].min())

    print "Least maxerr for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%i"%((P, maxerr.min()) + get_params_for_index(best_maxerr))
    print "Least error  for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%i"%((P, E[i].min()) + get_params_for_index(best))

    fig = plt.figure()
    ax = Axes3D(fig)

    X, Y = numpy.meshgrid(aa[1:], pp)
    Z = maxerr[1,:,1:,1,3]
    Z[numpy.where(Z > 1E17)] = None
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
    ax.set_title("Maxerr vs. a and p in L%i"%(P))
    ax.set_xlabel('a')
    ax.set_ylabel('p')
    ax.set_zlabel('E')
    fig.colorbar(surf)
    
plt.show()
