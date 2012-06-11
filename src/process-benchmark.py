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
                        print "Did not find n=%i, p=%i, a=%i, g=%i, s=%f"%(n,p,a,g,s)
                        continue
                    
                    absolute_errors = numpy.load(path)
                    absolute_rms_time = ((absolute_errors**2).mean(axis=2))**0.5
#                    print absolute_rms_time
#                    print absolute_rms_time.max(axis=0)
                    for i, norm in enumerate(err_norms):
                        E[i,ni,pi,ai,gi,si,:] = absolute_rms_time[:,i]

def get_params_for_index(index):
    return (nn[index[0]], pp[index[1]], aa[index[2]], gg[index[3]], ss[index[4]]/10.0)

for i, P in enumerate(err_norms[:1]):
    maxerr = E[i].max(axis=5)
    
    best_maxerr = numpy.where(maxerr == maxerr.min())
    best = numpy.where(E[i] == E[i].min())

    print "Least maxerr for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%f"%((P, maxerr.min()) + get_params_for_index(best_maxerr))
    print "Least error  for L%i: %f\tn=%i, p=%i, a=%i, g=%i, s=%f"%((P, E[i].min()) + get_params_for_index(best))

    import sys
    plottype = "surf"
    if len(sys.argv) > 1:
        plottype = sys.argv[1]

    ################################
    #            E_{p,a}           #
    ################################

    fig = plt.figure()
    ax = Axes3D(fig)

    mina = 1#1
    maxa = len(aa)
    minp = 0
    maxp = len(pp)

    if best_maxerr[0] == 3:
        maxp -= 1

    X = aa[mina:maxa]
    Y = pp[minp:maxp]

    X, Y = numpy.meshgrid(X, Y)
    print X
    print Y

    Z = maxerr[best_maxerr[0][0],minp:maxp,mina:maxa,best_maxerr[3][0],best_maxerr[4][0]]
    Z[numpy.where(Z > 1E17)] = None

    print Z

    def scatterplot():
        return ax.scatter(X.flatten(), Y.flatten(), Z.flatten())#, rstride=1, cstride=1, cmap=cm.jet)
    
    def surfplot():
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
        fig.colorbar(surf)
        return surf

    def wireframeplot():
        return ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)

    def plot(s):
        if s == "scatter":
            return scatterplot()
        if s == "surf":
            return surfplot()
        if s == "wireframe":
            return wireframeplot()
        raise TypeError("No such plot function.")

    plot(plottype)

    ax.set_title("Maxerr vs. a and p in L%i"%(P))
    ax.set_xlabel('a')
    ax.set_ylabel('p')
    ax.set_zlabel('E')


    ################################
    #            E_{s,g}           #
    ################################
    
    fig = plt.figure()
    ax = Axes3D(fig)

    mins = 0#2
    maxs = len(ss)-1
    ming = 0
    maxg = len(gg)

    X = numpy.array(ss[mins:maxs])/10.0
    Y = gg[ming:maxg]

    X, Y = numpy.meshgrid(X, Y)
    Z = maxerr[best_maxerr[0][0],best_maxerr[1][0],best_maxerr[2][0],ming:maxg,mins:maxs]
    Z[numpy.where(Z > 1E17)] = None
    print Z

    def scatterplot():
        return ax.scatter(X.flatten(), Y.flatten(), Z.flatten())#, rstride=1, cstride=1, cmap=cm.jet)
    
    def surfplot():
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)
        fig.colorbar(surf)
        return surf

    def wireframeplot():
        return ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet)

    def plot(s):
        if s == "scatter":
            return scatterplot()
        if s == "surf":
            return surfplot()
        if s == "wireframe":
            return wireframeplot()
        raise TypeError("No such plot function.")

    plot(plottype)

    ax.set_title("Maxerr vs. sigma and g in L%i"%(P))
    ax.set_xlabel('sigma')
    ax.set_ylabel('g')
    ax.set_zlabel('E')
    
    ################################
    #              E_n             #
    ################################
    
    fig = plt.figure()
    plt.semilogx(nn, maxerr[:,best_maxerr[1][0],best_maxerr[2][0],best_maxerr[3][0],best_maxerr[4][0]], nn, maxerr[:,best_maxerr[1][0],best_maxerr[2][0],best_maxerr[3][0],best_maxerr[4][0]], 'r*', basex=2)
    fig.get_axes()[0].set_xticklabels([str(2**n) for n in xrange(5,10)])
    plt.axis((2**5.75, 2**9.25, 0, 80))
    plt.xlabel('n')
    plt.ylabel('E')
    plt.title("Max error vs. number of particles")

plt.show()
