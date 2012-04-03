
import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen

from scipy.ndimage import filters

from wimageprocessing import gray,central_diff,filter_video

#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    #layermanager.add_layer(wvideo("../video/square_simple.pngvin",0.5)) #load video from file
    
    bounce=wvideo("../video/square_simple.pngvin/",0.5)    

    layermanager.add_layer(bounce) 



    blurbounce=wvideo("../video/square_simple.pngvin/",0.5)
    blurbounce.transform(lambda img: filters.gaussian_filter(img,10))
    print blurbounce
    layermanager.add_layer(blurbounce)

    #layermanager.add_layer(testscreen(5,0.4))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
