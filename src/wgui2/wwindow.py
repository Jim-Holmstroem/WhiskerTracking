import gtk
import pygtk

from wlayermanager import *

class wwindow(gtk.Window):
    __version__="0.2"
    program_name="WhiskerTracking"
    
    def __init__(self,layermanager=None,controller=None):
        gtk.Window.__init__(self)
        self.set_title(self.program_name+" - v"+self.__version__)
        self.connect("destroy",gtk.main_quit())

        vbox=gtk.VBox(False,0)
        hbox=gtk.HBox(False,0)

        self.add(gtk.status_icon_new_from_icon_name("gtk-yes"))
        if layermanager:
            vbox.add(layermanager)
            vbox.add(gtk.HScale(gtk.Adjustment(0,0,len(layermanager),1,1,1)
        else:
            vbox.add(gtk.image_new_from_stock("gtk-dialog-error",gtk.ICON_SIZE_DIALOG))
       
        hbox.add(vbox)

        if wcontroller:
            hbox.add(wcontroller)
        else:
            hbox.add(gtk.image_new_from_stock("gtk-dialog-error",gtk.ICON_SIZE_DIALOG))

        self.add(hbox)
        self.show_all()


