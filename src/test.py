import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen

import math
import numpy
import pylab

from common import make_video_path

from wview.gwhisker import GWhiskerLayer 


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
<<<<<<< HEAD
    whisker1=wvideo(map(lambda b:
        GWhiskerLayer((-0.0001,float(b)/2048,0,0),5,150,5,rotation=0.,translate=(256.,256.)),range(-16,16+1)),alpha=1.0)
#    whisker2=wvideo(map(lambda b:
#        GWhiskerLayer((0,-float(b)/2048,0,0),5,150,5,rotation=math.pi/4,translate=(256.,256.)),range(-16,16+1)),alpha=0.3)
#    whisker3=wvideo(map(lambda b:
#        GWhiskerLayer((0,float(b)/2048,0,0),5,150,5,rotation=-math.pi/4,translate=(256.,256.)),range(-16,16+1)),alpha=0.3)
    
    layermanager.add_layer(whisker1)
#    layermanager.add_layer(whisker2)
#    layermanager.add_layer(whisker3)
=======
    
    tries = 8

    testrange=range(-tries,tries+1)

    whisker3=wvideo(map(lambda b:
        GWhiskerLayer((float(b*(16/float(tries)))/(512**2),0,0,0),rotation=0,translate=(256.,256.)),testrange),alpha=0.3)
    whisker2=wvideo(map(lambda b:
        GWhiskerLayer((0,float(b*(16/float(tries)))/512,0,0),rotation=0,translate=(256.,256.)),testrange),alpha=0.3)
    whisker1=wvideo(map(lambda b:
        GWhiskerLayer((0,0,float(b*(16/float(tries)))/8,0),rotation=0,translate=(256.,256.)),testrange),alpha=0.3)
    zero=wvideo(map(lambda b:
        GWhiskerLayer((0,0,0,0),rotation=0.,translate=(256.,256.)),testrange),alpha=0.3)
    
    x1=numpy.array(map(lambda b:float(b*(16/float(tries)))/(512**2),testrange))
    x2=numpy.array(map(lambda b:float(b*(16/float(tries)))/512,testrange))
    x3=numpy.array(map(lambda b:float(b*(16/float(tries)))/8,testrange))
    
    
    #phi
    zerot=zero
    whisker1t=whisker1
    whisker2t=whisker2
    whisker3t=whisker3
   
    #correlation
    response1=numpy.array((zerot*whisker1t).sum())
    response2=numpy.array((zerot*whisker2t).sum())
    response3=numpy.array((zerot*whisker3t).sum())

    pylab.plot(x1,response1)
    pylab.show()

    pylab.plot(x2,response2)
    pylab.show()

    pylab.plot(x3,response3)
    pylab.show()

    layermanager.add_layer(whisker3)
    layermanager.add_layer(whisker2)
    layermanager.add_layer(whisker1)
>>>>>>> origin/presentation
  
    layermanager.exportPNGVIN(make_video_path("gwhisker_spline_test.pngvin"))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
