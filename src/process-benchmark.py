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
worst = numpy.ones(tensor_dim[:-1]) * 1E18

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
                        worst[i,ni,pi,ai,gi,si] = E[i,ni,pi,ai,gi,si,:].max()

def get_params_for_index(index):
    return (nn[index[0]], pp[index[1]], aa[index[2]], gg[index[3]], ss[index[4]])

for i, P in enumerate(err_norms):
    worst = E[i].max(axis=5)
    print worst.min()
    
    best = numpy.where(E[i] == E[i].min())
    best_worst = numpy.where(worst == worst.min())

    print "Least error for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%i"%((P, E[i].min()) + get_params_for_index(best))
    print "Least maximum error for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%i"%((P, E[i].min()) + get_params_for_index(best_worst))

    fig = plt.figure()
    ax = Axes3D(fig)
    X = aa[1:]
    Y = pp
    
    X, Y = numpy.meshgrid(X, Y)
    Z = E[i,1,:,1:,1,3,1]
    Z[numpy.where(Z > 1E17)] = None
    
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
    ax.set_zlim3d(0, 150)
    ax.w_zaxis.set_major_locator(LinearLocator(10))
    ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

    ax.set_title("")
    ax.set_xlabel('a')
    ax.set_ylabel('p')
    ax.set_zlabel('E')
    
    fig.colorbar(surf)
    
plt.show()
