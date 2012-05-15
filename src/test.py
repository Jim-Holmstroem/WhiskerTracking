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
