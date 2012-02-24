import gtk
import pygtk
import cairo

class wlayermanager(gtk.DrawingArea):

    __layers=[]

    def __init__(self):
        super(wlayermanager,self).__init__()
        #gtk.DrawingArea.__init__(self)
        self.connect("expose_event",self.expose)

    def add_layer(self,layer,zindex=None):
        if type(layer) is list:
            self.__layers.extend(layer) #if multiple lists 
        else:
            if zindex:
                self.__layers.insert(zindex,layer)
            else:
                self.__layers.append(layer)

    def remove_layer(self,layer):
        self.__layers.remove(layer)

    def expose(self,widget,event):
        self.context = widget.window.cairo_create()
        
        for layer in self.__layers:
            layer.draw(self.context)
        
        self.draw(self.context)
        return False


