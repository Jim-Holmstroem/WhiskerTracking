
__init__ = ['wwindow']

import gtk
import pygtk

from wgui.wlayermanager import wlayermanager

class wwindow(gtk.Window):
    __version__="0.2"
    program_name="WhiskerTracking"
    
    def __init__(self,layermanager=None,controller=None):
        self.layermanager=layermanager
        self.controller=controller
        
        gtk.Window.__init__(self)
        self.set_title(self.program_name+" - v"+self.__version__)
        self.connect("destroy",gtk.main_quit)
        vbox=gtk.VBox(False,0)
        hbox=gtk.HBox(False,0)

        if layermanager:
            vbox.add(layermanager)
        else:
            error=gtk.image_new_from_stock("gtk-dialog-error",gtk.ICON_SIZE_DIALOG)
            error.set_size_request(512,512)
            vbox.add(error)

        timeline=gtk.Adjustment(0,0,len(layermanager),1,1,1)
        timeline.connect("value-changed",self.timeline_changed)
        timescale=gtk.HScale(timeline)
        timescale.set_digits(0)

        vbox.add(timescale)
        hbox.add(vbox)

        if controller:
            hbox.add(controller)
        else:
            hbox.add(gtk.image_new_from_stock("gtk-dialog-error",gtk.ICON_SIZE_DIALOG))

        self.add(hbox)
        self.show_all()

    def timeline_changed(self,adjustment):
        self.layermanager.set_current_frame(int(adjustment.get_value()))
