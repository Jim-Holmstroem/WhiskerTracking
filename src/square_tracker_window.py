
import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen
from wimageprocessing import normalize

from scipy.ndimage import filters

import math
import numpy


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    #layermanager.add_layer(wvideo("../video/square_simple.pngvin",0.5)) #load video from file
    
    bounce=wvideo("../video/square_simple.pngvin",0.2)
    #layermanager.add_layer(bounce) 

    blur5 = lambda img: filters.gaussian_filter(img,5)

    blurbounce=bounce.transform(blur5)
 #   edge_filter=filters.prewitt
 #   abs_edge_filter=lambda img:numpy.sqrt(edge_filter(img,axis=0)**2+edge_filter(img,axis=1)**2)
 #   edgebounce=blurbounce.transform(abs_edge_filter)
    
    #badedgebounce=bounce.transform(abs_edge_filter)
    #bluredbadedgebounce=badedgebounce.transform(blur5)
    #layermanager.add_layer(bluredbadedgebounce.transform(normalize))
    
    #layermanager.add_layer(wvideo(testscreen(alpha=0.1)))



    #layermanager.add_layer(wvideo(testscreen(alpha=0.5)))
    #layermanager.add_layer(testscreen(alpha=0.1))
   
    layermanager.add_layer(blurbounce)
    layermanager.add_layer(testscreen(alpha=0.5))

    #layermanager.add_layer(multiply.transform(normalize))
  

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
