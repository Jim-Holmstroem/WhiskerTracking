__all__ = ['wlayermanager']

import gtk
import cairo
import os
import re
from common import settings

def video_format_filename(i):
    """Get a frame filename for the given integer
    @return: "frame-" followed by i. i will be padded with zeroes to length 5.
    """
    return "frame-%05d.png"%(i)

class wlayermanager(gtk.DrawingArea):
    """
    Contains all the layers and controlls the rendering and exporting
    """

    layers=[]
    current_frame=0

    def __init__(self,layers=None, width=settings.IMAGE_WIDTH, height=settings.IMAGE_HEIGHT):
        """
        Arguments: layers either one layer or multiple
        """
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event",self.expose)
        self.connect("motion-notify-event",self.motion)
        self.set_size_request(width,height)
        
        if not layers is None:
            map(lambda l:self.add_layer(l), layers)

    def render_layer(self,context,layer,i):
        """
        Used by renderer to render each layer
        """
        context.save()
        layer.render(context,i)
        context.restore()

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
    
    def expose(self,widget,event,width=settings.IMAGE_WIDTH,height=settings.IMAGE_HEIGHT):
        """

        """
        context=widget.window.cairo_create()

        context.set_source_rgba(0,0,0,1)
        context.rectangle(0,0,width,height)
        context.fill()
        
        self.render(context,self.current_frame)

    
    def __len__(self):
        """
        The maximum number of frames needed to render this.
        """
        if len(self.layers)==0:
            return 0
        return max(map(lambda layer:len(layer),self.layers))

    def exportPNGVIN(self,video_dir=None, width=settings.IMAGE_WIDTH, height=settings.IMAGE_HEIGHT):
        """

        """
        assert re.match(".+\.(PNGVIN|pngvin)$",video_dir)
        #The index of the file is saved as the first element in the pair
        surfaces=map(lambda frame:(frame,cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)),xrange(len(self)))
        contexts=map(lambda surface:(surface[0],cairo.Context(surface[1])),surfaces)
        map(lambda context:self.render(context[1],context[0]),contexts)
        
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        
        map(lambda surface:surface[1].write_to_png(os.path.join(video_dir, video_format_filename(surface[0]))), surfaces)

    def motion(self,widget,event):
        """
        Gets the mousemovement inside the drawingarea
        """
        print "motion"

        
