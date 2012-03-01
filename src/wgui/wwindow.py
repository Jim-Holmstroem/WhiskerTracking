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
        self.connect("destroy",gtk.main_quit)
        
        vbox = gtk.VBox(False,0)
        hbox = gtk.HBox(False,0)
        
        vbox.add(layermanager)

        vbox.add(gtk.HScale(gtk.Adjustment(0,0,32,1,1,1)))
        
        hbox.add(vbox)


        btn = gtk.Button("Knappis")
        #TODO button to activate som plotting of values in current frame`

        hbox.add(btn)
        
        
        self.add(hbox)
        
        self.show_all()




if __name__=="__main__":
    
    layermanager = wlayermanager()
    layermanager.add_layer(wimagelayer())
    layermanager.add_layer(wtestlayer())
    
    win=wwindow(layermanager)
   
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
