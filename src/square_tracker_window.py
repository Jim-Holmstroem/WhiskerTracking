
import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen

from wimageprocessing import central_diff,filter_video

#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
#    layermanager.add_layer(wvideo("../video/square_simple.pngvin",0.5)) #load video from file
    
    
    bounce=wvideo("../video/square_simple.pngvin/",0.5)
    layermanager.add_layer(bounce) #load video from file
    diffbounce=filter_video(bounce,lambda img:central_diff(img)[0]) 
    


    layermanager.add_layer(testscreen(5,0.4))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
