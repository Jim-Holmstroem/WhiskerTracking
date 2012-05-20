import gtk

from wgui import wwindow,wlayermanager
from wmedia import wimage,wvideo,testscreen

import math
import numpy
import pylab
import scipy

from common import make_video_path

from wview.gwhisker import GWhiskerLayer 


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    
    tries = 64*4

    testrange=range(-tries,tries+1)
    testalpha=0.3


    pos=(272.,126.)
    w=3

    whisker3=wvideo(map(lambda b:
        GWhiskerLayer((float(b*(16/float(tries)))/(512**2),0,0,0),rotation=0,width=w,translate=pos),testrange),alpha=testalpha)
    whisker2=wvideo(map(lambda b:
        GWhiskerLayer((0,float(b*(16/float(tries)))/512,0,0),rotation=0,width=w,translate=pos),testrange),alpha=testalpha)
    whisker1=wvideo(map(lambda b:
        GWhiskerLayer((0,0,float(b*(16/float(tries)))/8,0),rotation=0,width=w,translate=pos),testrange),alpha=testalpha)

    testimage=wimage("/misc/projects/whisker/video/m8_multi-frames/preprocessed_whiskers/frame-0488.png")
    zero=wvideo([testimage]*len(testrange),alpha=testalpha)
    
    x1=numpy.array(map(lambda b:float(b*(16/float(tries)))/(512**2),testrange))
    x2=numpy.array(map(lambda b:float(b*(16/float(tries)))/512,testrange))
    x3=numpy.array(map(lambda b:float(b*(16/float(tries)))/8,testrange))
    
    #phi
    zerot=zero
    whisker1t=whisker1
    whisker2t=whisker2
    whisker3t=whisker3

    #trans = scipy.ndimage.laplace

    #zerot=zero.transform(trans)
    #whisker1t=whisker1.transform(trans)
    #whisker2t=whisker2.transform(trans)
    #whisker3t=whisker3.transform(trans)
    
    normalize=zerot[0].sum() #OK since static

    #correlation
    response1=numpy.array((zerot*whisker1t).sum())/normalize
    response2=numpy.array((zerot*whisker2t).sum())/normalize
    response3=numpy.array((zerot*whisker3t).sum())/normalize

    ymax = max([max(response1),max(response2),max(response3)])

    pylab.figure(1)
    
    pylab.subplot(131)
    pylab.plot(x1,response1)
    pylab.axis([-0.00008,0.00008,0,ymax])
    pylab.title('a3')

    a=pylab.gca()
    a.xaxis.set_ticks([-0.00008,-0.00004,0.0,0.00004,0.00008])
    
    pylab.subplot(132) 
    pylab.plot(x2,response2)
    pylab.axis([-0.04,0.04,0,ymax])
    pylab.title('a2')
    
    pylab.subplot(133) 
    pylab.plot(x3,response3)
    pylab.axis([-2,2,0,ymax])
    pylab.title('a1')

    pylab.show()

    layermanager.add_layer(testimage)
    layermanager.add_layer(whisker1)
    layermanager.add_layer(whisker2)
    layermanager.add_layer(whisker3)
  
    #layermanager.exportPNGVIN(make_video_path("gwhisker_spline_test.pngvin"))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
