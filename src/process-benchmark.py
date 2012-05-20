import numpy
import os
import pylab
import sys

absolute_error_path_pattern = "/misc/projects/whisker/results/GWhiskerTracker_n=%i_p=%i_a=%i_g=%i_s=%s/absolute_error.npy"

sigma_limits = numpy.array((0.000016, 0.004, 1))/10

nn = (64, 128, 256, 512)
pp = (2, 4, 8)
aa = (1, 2, 4, 8)
gg = (1, 2, 4, 8)
ss = (0.25, 0.5, 1, 2)

pylab.figure(1)
pylab.title("Worst error versus $a$, varying $p$")

E = numpy.ones((len(nn), len(pp), len(aa), len(gg), len(ss))) * 1E18
E_l4 = numpy.ones((len(nn), len(pp), len(aa), len(gg), len(ss))) * 1E18
E_l8 = numpy.ones((len(nn), len(pp), len(aa), len(gg), len(ss))) * 1E18

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
                    absolute_sum_time = absolute_errors.sum(axis=2)
                    absolute_rms_time = ((absolute_errors**2).mean(axis=2))**0.5
                    #worst = absolute_sum_time.max(axis=0)
                    worst = absolute_rms_time.max(axis=0)
                    #print absolute_errors
                    #print absolute_rms_time
                    #print worst
                    E[ni,pi,ai,gi,si], E_l4[ni,pi,ai,gi,si], E_l8[ni,pi,ai,gi,si] = worst
                    

win = numpy.where(E == E.min())
print "Best results for L2: %f\tn=%i, p=%i, a=%i, g=%i, s=%f"%(E.min(), nn[win[0]],pp[win[1]],aa[win[2]],gg[win[3]],ss[win[4]])

win_l4 = numpy.where(E_l4 == E_l4.min())
print "Best results for L4: %f\tn=%i, p=%i, a=%i, g=%i, s=%f"%(E_l4.min(), nn[win[0]],pp[win[1]],aa[win[2]],gg[win[3]],ss[win[4]])

win_l8 = numpy.where(E_l8 == E_l8.min())
print "Best results for L8: %f\tn=%i, p=%i, a=%i, g=%i, s=%f"%(E_l8.min(), nn[win[0]],pp[win[1]],aa[win[2]],gg[win[3]],ss[win[4]])

sys.exit()


pylab.loglog(erra, err, '-*', basex=2, basey=10, label="$N$=%i, $p$=%i"%(E[n,p]))

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

