
__all__ = ['wlayermanager']

import gtk
import pygtk
import cairo

class wlayermanager(gtk.DrawingArea):
    """
    Contains all the layers and controlls the rendering and exporting
    """

    layers=[]
    current_frame=0

    def __init__(self,layers=None):
        """
        Arguments: layers either one layer or multiple
        """
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event",self.expose)
        self.connect("motion-notify-event",self.motion)
        self.set_size_request(512,512)

    def set_current_frame(self,i):
        self.current_frame=i
    def next_frame(self):
        self.current_frame+=1
    def prev_frame(self):
        self.current_frame-=1

    def render_layer(self,context,layer,i):
        """
        Used by renderer to render each layer
        """
        layer.render(context,i)
        context.paint_with_alpha(layer.alpha)

    def render(self,context,i):
        """
        Renders all the layers with frame i on context     
        """
        map(lambda layer:self.render_layer(context,layer,i),self.layers)
    
    def add_layer(self,layer,i=None):
        if i is None:
            self.layers.append(layer)
        else:
            self.layers.insert(i,layer)

    def set_current_frame(self,i):
        self.current_frame=i
        self.queue_draw() #queue the redrawing of this drawingarea
    
    def expose(self,widget,event):
        """

        """
        context=widget.window.cairo_create()
        self.render(context,self.current_frame)
    
    def __len__(self):
        """
        The maximum number of frames needed to render this.
        """
        if len(self.layers)==0:
            return 0
        return max(map(lambda layer:len(layer),self.layers))

    def exportPNGVIN(self,filename=None):
        """

        """
        #The index of the file is saved as the first element in the pair
        surfaces=map(lambda frame:(frame,cairo.ImageSurface(FORMAT_ARGB32,WIDTH,HEIGHT)),xrange(len(self)))
        contexts=map(lambda surface:(surface[0],cairo.Context(surface[1])),surfaces)
        map(lambda context:self.render(context[1],context[0]),contexts)
        map(lambda surface:surface[1].write_to_png(filename+helper.video_format_filename(surface[0])),surfaces)

    def motion(self,widget,event):
        """
        Gets the mousemovement inside the drawingarea
        """
        print "motion"

        
