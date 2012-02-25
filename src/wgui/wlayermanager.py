import gtk
import pygtk
import cairo

class wlayermanager(gtk.DrawingArea):

    __layers=[]

    def __init__(self):
        super(wlayermanager,self).__init__()
        self.connect("expose_event",self.expose)
        self.set_size_request(512,512) 
        

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

#    def configure_event(self,widget,event):
#        print "configure_event()=changed size on widget"

    def expose(self,widget,event):
        self.context = widget.window.cairo_create()
        
        for layer in self.__layers:
            layer.draw(self.context)     
        
        #think we need widget.queue_draw_area(rectangle)
        #self.context.rectangle(event.area.x, event.area.y,event.area.width, event.area.height)
        #self.context.clip()

        #self.draw(self.context) ?? why cant i do this?
        return False


