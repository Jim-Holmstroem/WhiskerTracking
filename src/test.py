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

    whisker=wvideo(map(lambda b:GWhiskerLayer((0,float(b)/10,0,150)),range(-36,36)))
    layermanager.add_layer(whisker)
  
    layermanager.exportPNGVIN(make_video_path("gwhisker_spline_test.pngvin"))

    win=wwindow(layermanager)

    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
