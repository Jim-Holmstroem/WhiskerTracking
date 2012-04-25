
__all__ = ['wcontroller']

import gtk

class wcontroller(gtk.Widget):
    def __init__(self,layermanager):
        gtk.Widget.__init__(self)
        self.layermanager = layermanager

