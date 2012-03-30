from wgui2.wwindow import *
from wgui2.wlayermanager import *
from wmedia2.wvideo import *
from wmedia2.modelanimations import *


#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    layermanager.add_layer(wvideo("/misc/projects/whisker/video/square_simple.pngvin")) #load video from file
    
    layermanager.add_layer(testscreen())

    win=wwindow(layermanager)


    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
