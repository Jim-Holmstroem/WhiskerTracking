
import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen

from scipy.ndimage import filters

import math
import numpy


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    #layermanager.add_layer(wvideo("../video/square_simple.pngvin",0.5)) #load video from file
    
    bounce=wvideo("../video/square_simple.pngvin/",0.5)    
    #layermanager.add_layer(bounce) 

    blurbounce=bounce.transform(lambda img: filters.gaussian_filter(img,3))
    edgebounce=blurbounce.transform(lambda img:numpy.sqrt(filters.prewitt(img,axis=0)**2+filters.prewitt(img,axis=1)**2))
    layermanager.add_layer(blurbounce)
    layermanager.add_layer(edgebounce)

    layermanager.add_layer(testscreen(5,0.4))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
