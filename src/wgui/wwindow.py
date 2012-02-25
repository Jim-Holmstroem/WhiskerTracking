import gtk
import pygtk

from wlayermanager import *
from wimagelayer import *
from wtestlayer import *

class wwindow(gtk.Window):

    __version__="0.1"
    __program_name="WhiskerTracking"
    def __init__(self,layermanager):
        gtk.Window.__init__(self)
        self.set_title(self.__program_name+" - v"+self.__version__)
        self.set_default_size(1024,768)
        self.connect("destroy",gtk.main_quit)
        
        self.add(layermanager)
        
        self.show_all()

if __name__=="__main__":
    
    layermanager = wlayermanager()
    layermanager.add_layer(wimagelayer())
    layermanager.add_layer(wtestlayer())
    
    win=wwindow(layermanager)
   
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
