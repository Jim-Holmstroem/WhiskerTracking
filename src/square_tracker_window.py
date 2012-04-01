
import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    layermanager.add_layer(wvideo("../video/square_simple.pngvin")) #load video from file
    
    #layermanager.add_layer(testscreen(5))

    win=wwindow(layermanager)


    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
