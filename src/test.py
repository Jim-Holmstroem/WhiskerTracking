import gtk

from wgui import wwindow,wlayermanager
from wmedia import wvideo,testscreen

import math
import numpy

from common import make_video_path

from wview.gwhisker import GWhiskerLayer 

#selftest
if __name__=="__main__":
    layermanager = wlayermanager()
    whisker1=wvideo(map(lambda b:
        GWhiskerLayer((0,float(b)/2048,0,0),rotation=0.,translate=(256.,256.)),range(-16,16+1)),alpha=0.3)
    whisker2=wvideo(map(lambda b:
        GWhiskerLayer((0,-float(b)/2048,0,0),rotation=math.pi/4,translate=(256.,256.)),range(-16,16+1)),alpha=0.3)
    whisker3=wvideo(map(lambda b:
        GWhiskerLayer((0,float(b)/2048,0,0),rotation=-math.pi/4,translate=(256.,256.)),range(-16,16+1)),alpha=0.3)
    
    layermanager.add_layer(whisker1)
    layermanager.add_layer(whisker2)
    layermanager.add_layer(whisker3)
  
    layermanager.exportPNGVIN(make_video_path("gwhisker_spline_test.pngvin"))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
