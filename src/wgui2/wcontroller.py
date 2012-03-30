import gtk
import pygtk

class wcontroller(gtk.Widget):
    def __init__(self,layermanager):
        gtk.Wideget.__init__(self)
        self.layermanager = layermanager

