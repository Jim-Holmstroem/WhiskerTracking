import numpy
import os
import pylab
import sys

absolute_error_path_pattern = "/misc/projects/whisker/results/GWhiskerTracker_n=%i_p=%i_a=%i_g=4_s=[  4.00000000e-06   1.00000000e-03   5.00000000e-02]/absolute_error.npy"

nn = (64, 128, 256, 512)
pp = (2, 4, 8)
aa = (1, 2, 4, 8)

pylab.figure(1)
pylab.title("Worst error versus $a$, varying $p$")
for n in (512,):
    for p in pp:
        
        erra = []
        err = []
        
        for a in aa:
            path = absolute_error_path_pattern%(n, p, a)
            if not os.path.exists(path):
                continue

            absolute_errors = numpy.load(path)
            absolute_rms_time = ((absolute_errors**2).mean(axis=2))**0.5
            worst = absolute_rms_time.max(axis=0)

            erra.append(a)
            err.append(worst[0])
                
        pylab.loglog(erra, err, '-*', basex=2, basey=10, label="$N$=%i, $p$=%i"%(n,p))

pylab.xlabel("a")
pylab.ylabel("Worst error")
pylab.legend()
pylab.axis((2**-0.2, 2**3.2, 10, 10**3))


pylab.figure(2)
pylab.title("Worst error versus $a$, varying $N$")
for n in nn:
    for p in (4,):
        
        erra = []
        err = []
        
        for a in aa:
            path = absolute_error_path_pattern%(n, p, a)
            if not os.path.exists(path):
                continue

            absolute_errors = numpy.load(path)
            absolute_rms_time = ((absolute_errors**2).mean(axis=2))**0.5
            worst = absolute_rms_time.max(axis=0)

            erra.append(a)
            err.append(worst[0])
                
        pylab.loglog(erra, err, '-*', basex=2, basey=10, label="$N$=%i, $p$=%i"%(n,p))

pylab.xlabel("$a$")
pylab.ylabel("Worst error")
pylab.legend()
pylab.axis((2**-0.2, 2**3.2, 10, 10**3))


pylab.show()

